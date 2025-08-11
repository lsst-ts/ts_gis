__all__ = ["GISCsc", "execute_csc"]

import asyncio
import pathlib
from types import SimpleNamespace
from dataclasses import asdict

from lsst.ts import salobj
from lsst.ts import utils
from lsst.ts.xml import sal_enums
from pymodbus.server.simulator.http_server import ModbusSimulatorServer
from pymodbus.pdu import ModbusPDU

from . import __version__, enums
from .component import GISComponent
from .enums import subsystem_order
from .config import CONFIG_SCHEMA

FILE = pathlib.Path(__file__).resolve().parents[0] / "data" / "setup.json"


def execute_csc() -> None:
    asyncio.run(GISCsc.amain(index=None))


class GISCsc(salobj.ConfigurableCsc):
    """Implement the GIS CSC.

    Parameters
    ----------
    initial_state : `lsst.ts.salobj.State`
        The initial state that the CSC starts in.
    override : `str`
        The name of the config file.
    simulation_mode : `int`
        Is the GIS in simulation mode?
    config_dir : `pathlib.Path`
        The custom configuration file directory.

    Attributes
    ----------
    mock_server : `pymodbus.server.ModbusTcpServer`
        The mock modbus server.
        Just returns static values.
    component : `GISComponent`
        Handles the data received from the GIS.
    telemetry_interval : `float`
        The time to sleep for telemetry publishing.
    telemetry_task : `asyncio.Future`
        An asyncio task to handle starting and cancelling the telemetry loop.
    """

    valid_simulation_modes = [0, 1]
    version = __version__

    def __init__(
        self,
        initial_state: sal_enums.State | int = sal_enums.State.STANDBY,
        override: str = "",
        simulation_mode: int = 0,
        config_dir: None | pathlib.Path = None,
    ) -> None:
        super().__init__(
            name="GIS",
            index=None,
            config_schema=CONFIG_SCHEMA,
            initial_state=initial_state,
            override=override,
            simulation_mode=simulation_mode,
            config_dir=config_dir,
        )
        self.mock_server: None | ModbusSimulatorServer = None
        self.component: GISComponent = GISComponent(log=self.log, simulation_mode=self.simulation_mode)
        self.simulator: None = None
        self.telemetry_interval: int = self.heartbeat_interval
        self.telemetry_task: asyncio.Future[None] = utils.make_done_future()
        self.mock_server_task: asyncio.Future[None] = utils.make_done_future()

    async def telemetry_loop(self) -> None:
        """Implement the telemetry feed for the GIS."""
        self.log.info("Starting telemetry loop.")
        while True:
            try:
                if self.connected:
                    reply, status_string = await self.component.update_status()
                    assert status_string is not None
                    assert reply is not None
                    await self.evt_rawStatus.set_write(status=status_string)
                    await self.fill_out_fields(status_string)
                    await self.publish_new_subsystems(reply)
                    await asyncio.sleep(self.telemetry_interval)
                else:
                    await self.fault(code=1, report="Unexpectedly disconnected from GIS.")
                    return
            except Exception:
                self.log.exception("Telemetry loop failed.")

    async def publish_new_subsystems(self, reply: ModbusPDU) -> None:
        self.log.debug(f"registers={reply.registers}")
        for index, current_subsystem in enumerate(reply.registers):
            old_subsystem = self.component.system_status[index]
            if current_subsystem != old_subsystem:
                self.component.system_status[index] = current_subsystem
                await self.evt_systemStatus.set_write(index=index, status=current_subsystem)

    async def fill_out_fields(self, statuses: str) -> None:
        """Fill out subsystem event data.

        Iterate through the subsystem 1's and 0's array to publish each
        subsystem's boolean status.
        Some subsystem's have free reserved for future use and the XML has
        a count field greater than one for those blocks.
        The data classes use a tuple field to indicate the appropriate values
        for that XML item.
        Some data classes do not contain any tuples and so can be appended
        to the array as normal.

        Parameters
        ----------
        statuses: `str`
            The string array of 1's and 0's that comprise the status of the
            GIS's subsystems.
        """
        statuses_array = statuses.split(" ")
        for status_index, status in enumerate(statuses_array):
            self.log.debug(f"{status=}")
            subsystem_name = getattr(enums, subsystem_order[status_index])
            # For a given string of 1 and 0's, return an array of booleans
            if hasattr(subsystem_name, "tuple_range"):
                tuple_min, tuple_max = subsystem_name.tuple_range()
            else:
                tuple_min = tuple_max = None
            t: tuple[bool, ...] = tuple()
            status_as_bool: list[tuple[bool, ...] | bool] = []
            appended_tuple = False
            for bit_index, bit_status in enumerate(status):
                if tuple_max is not None and tuple_min is not None:
                    if bit_index >= tuple_min and bit_index < tuple_max:
                        t += tuple([bool(int(bit_status))])
                    elif bit_index + 1 > tuple_max and not appended_tuple:
                        t += tuple([bool(int(bit_status))])
                        status_as_bool.append(t)
                        appended_tuple = True
                    else:
                        status_as_bool.append(bool(int(bit_status)))
                else:
                    status_as_bool.append(bool(int(bit_status)))
            self.log.debug(f"{status_as_bool=}")
            # Instantiate the data class with the boolean arguments
            subsystem_data = subsystem_name(*status_as_bool)
            subsystem_event = getattr(self, f"evt_{subsystem_order[status_index]}")
            await subsystem_event.set_write(**asdict(subsystem_data))

    @property
    def connected(self) -> bool:
        """Return whether the component is connected."""
        return self.component.connected

    async def handle_summary_state(self) -> None:
        """Handle summary state transitions.

        When transitioning to disabled or enabled state.
        * Connect to the client if not connected.
        * Start the mock server if in simulation mode and not started.
        * Start the telemetry loop if not started.

        When outside of the disabled or enabled state.

        * disconnect from the client if connected.
        * Close the mock server if running.
        * Cancel the telemetry loop.
        """
        if self.disabled_or_enabled:
            if self.simulation_mode and self.mock_server is None:
                self.mock_server = ModbusSimulatorServer(json_file=FILE.as_posix())
                self.log.info("Starting mock server.")
                if self.mock_server_task.done():
                    self.mock_server_task = asyncio.create_task(
                        self.mock_server.run_forever(only_start=False)
                    )
                    await asyncio.sleep(0.5)
            if not self.connected:
                self.log.info("Connect to the GIS.")
                await self.component.connect()
            if self.telemetry_task.done():
                self.telemetry_task = asyncio.create_task(self.telemetry_loop())
        else:
            self.telemetry_task.cancel()
            await self.component.disconnect()
            self.mock_server_task.cancel()
            if self.mock_server is not None:
                await self.mock_server.stop()
                self.mock_server = None

    async def configure(self, config: SimpleNamespace) -> None:
        """Configure the GIS."""
        self.telemetry_interval = config.telemetry_interval
        self.component.configure(config)

    @staticmethod
    def get_config_pkg() -> str:
        """Return the name of the configuration repository."""
        return "ts_config_ocs"

    async def close_tasks(self) -> None:
        """Shutdown mock server and connection to server."""
        await self.component.disconnect()
        self.telemetry_task.cancel()
        self.mock_server_task.cancel()
        if self.mock_server is not None:
            await self.mock_server.stop()
            self.mock_server = None
        await super().close_tasks()
