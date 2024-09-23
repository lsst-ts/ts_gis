__all__ = ["GISCsc", "execute_csc"]

import asyncio
import pathlib

from lsst.ts import salobj, utils
from pymodbus.server.simulator.http_server import ModbusSimulatorServer

from . import __version__
from .component import GISComponent
from .config import CONFIG_SCHEMA

FILE = pathlib.Path(__file__).resolve().parents[0] / "data" / "setup.json"


def execute_csc():
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
        initial_state=salobj.State.STANDBY,
        override=None,
        simulation_mode=False,
        config_dir=None,
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
        self.mock_server = None
        self.component = GISComponent(self)
        self.simulator = None
        self.telemetry_interval = None
        self.telemetry_task = utils.make_done_future()
        self.mock_server_task = utils.make_done_future()

    async def telemetry_loop(self):
        """Implement the telemetry feed for the GIS."""
        self.log.info("Starting telemetry loop.")
        while True:
            try:
                if self.connected:
                    await self.component.update_status()
                    await asyncio.sleep(self.telemetry_interval)
                else:
                    await self.fault(
                        code=1, report="Unexpectedly disconnected from GIS."
                    )
            except Exception:
                self.log.exception("Telemetry loop failed.")
                raise

    @property
    def connected(self):
        """Return whether the component is connected."""
        return self.component.connected

    async def handle_summary_state(self):
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
                self.mock_server = ModbusSimulatorServer(json_file=FILE)
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

    async def configure(self, config):
        """Configure the GIS."""
        self.telemetry_interval = config.telemetry_interval
        self.component.configure(config)

    @staticmethod
    def get_config_pkg():
        """Return the name of the configuration repository."""
        return "ts_config_ocs"

    async def close_tasks(self):
        """Shutdown mock server and connection to server."""
        await self.component.disconnect()
        self.telemetry_task.cancel()
        self.mock_server_task.cancel()
        if self.mock_server is not None:
            await self.mock_server.stop()
            self.mock_server = None
        await super().close_tasks()
