__all__ = ["GISCsc", "execute_csc", "command_csc"]

import asyncio
import dataclasses
import json
import pathlib
import socket
import tempfile
from dataclasses import asdict
from typing import Any

from pymodbus.pdu import ModbusPDU
from pymodbus.server.simulator.http_server import ModbusSimulatorServer

from lsst.ts import salobj, utils
from lsst.ts.xml import sal_enums

from . import __version__, enums
from .component import GISComponent
from .config import CONFIG_SCHEMA, GISConfig
from .enums import ErrorCode, subsystem_order
from .wizardry import BITS_PER_REGISTER

SIMULATOR_SETUP_FILE = pathlib.Path(__file__).resolve().parents[0] / "data" / "setup.json"
LOCALHOST = "127.0.0.1"
"""Local host address used for simulation-only services."""
SIMULATOR_START_TIMEOUT = 2.0
"""Seconds to wait for the Modbus simulator to report that it started."""


def command_csc() -> None:
    """Command the GIS CSC."""
    asyncio.run(salobj.CscCommander.amain(name="GIS", index=None))


def execute_csc() -> None:
    """Run the GIS CSC."""
    asyncio.run(GISCsc.amain(index=None))


def get_free_tcp_port(host: str = LOCALHOST) -> int:
    """Return an available TCP port for local simulation.

    This is best-effort: the socket is released before the
    simulator binds, so another process could theoretically claim the port.
    The helper is only used for local simulation startup.

    Parameters
    ----------
    host : `str`, optional
        Host interface on which to search for an available port.

    Returns
    -------
    port : `int`
        Available TCP port number.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return sock.getsockname()[1]


def make_simulator_setup_json(source: pathlib.Path, port: int) -> pathlib.Path:
    """Create a temporary simulator JSON file with the selected Modbus port.

    Parameters
    ----------
    source : `pathlib.Path`
        Path to the base pymodbus simulator JSON file.
    port : `int`
        Modbus TCP port to write into the temporary simulator JSON file.

    Returns
    -------
    path : `pathlib.Path`
        Path to the temporary simulator JSON file.

    Raises
    ------
    OSError
        Raised if the source file cannot be read or the temporary file cannot
        be written.
    json.JSONDecodeError
        Raised if ``source`` is not valid JSON.
    """
    setup = json.loads(source.read_text())

    # setup.json currently stores this as a string
    setup["server_list"]["server"]["port"] = str(port)

    tmp = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", suffix=".json", prefix="gis-simulator", delete=False
    )
    with tmp:
        json.dump(setup, tmp)

    return pathlib.Path(tmp.name)


def make_subsystem_kwargs(subsystem_type: type, bits: list[int]) -> dict[str, bool | tuple[bool, ...]]:
    """Map decoded register bits to dataclass constructor keyword arguments.

    Free/reserved bit ranges declared by a subsystem's ``tuple_range`` method
    are packed into the corresponding tuple field.
    All other bits are mapped one-to-one to dataclass fields in field order.

    Parameters
    ----------
    subsystem_type : `type`
        Dataclass type from `lsst.ts.gis.enums` that represents one GIS
        subsystem event.
    bits : `list` [`int`]
        Decoded bits for one Modbus register, ordered from bit 0 to bit 15.

    Returns
    -------
    kwargs : `dict` [`str`, `bool` or `tuple` [`bool`, ...]]
        Keyword arguments suitable for constructing ``subsystem_type``.

    Raises
    ------
    ValueError
        Raised if ``bits`` does not contain exactly one register of decoded
        bit values, or if the dataclass fields do not consume all bits.
    """
    if len(bits) != BITS_PER_REGISTER:
        raise ValueError(f"Expected {BITS_PER_REGISTER} bits, got {len(bits)}.")
    values = [bool(bit) for bit in bits]
    fields = dataclasses.fields(subsystem_type)

    tuple_range = subsystem_type.tuple_range() if hasattr(subsystem_type, "tuple_range") else None

    kwargs: dict[str, bool | tuple[bool, ...]] = {}

    bit_index = 0
    for field in fields:
        if tuple_range is not None and bit_index == tuple_range[0]:
            start, stop = tuple_range
            kwargs[field.name] = tuple(values[start:stop])
            bit_index = stop
        else:
            kwargs[field.name] = values[bit_index]
            bit_index += 1

    if bit_index != len(bits):
        raise ValueError(
            f"{subsystem_type.__name__} consumed {bit_index} bits, but received {len(bits)} bits."
        )

    return kwargs


def make_subsystem_data(subsystem_type: type, bits: list[int]) -> Any:
    """Create a subsystem dataclass instance from decoded register bits.

    Parameters
    ----------
    subsystem_type : `type`
        Dataclass type from `lsst.ts.gis.enums` that represents one GIS
        subsystem event.
    bits : `list` [`int`]
        Decoded bits for one Modbus register, ordered from bit 0 to bit 15.

    Returns
    -------
    subsystem : `object`
        The constructed subsystem instance.

    Raises
    ------
    ValueError
        Raised if the decoded bits cannot be mapped to ``subsystem_type``.
    """
    kwargs = make_subsystem_kwargs(subsystem_type, bits)
    return subsystem_type(**kwargs)


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
    mock_server : `ModbusSimulatorServer` or `None`
        The mock modbus server.
    component : `GISComponent`
        Handles the data received from the GIS.
    simulator : `None`
        Placeholder for simulator state.
    telemetry_interval : `float`
        The time to sleep between telemetry publications.
    telemetry_task : `asyncio.Future` [`None`]
        The task that runs the telemetry loop.
    mock_server_task : `asyncio.Future` [`None`]
        The task that runs the mock server.
    mock_server_setup_file : `pathlib.Path` or `None`
        Temporary simulator JSON file used in simulation mode.
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
        self.telemetry_interval: float = self.heartbeat_interval
        self.telemetry_task: asyncio.Future[None] = utils.make_done_future()
        self.mock_server_task: asyncio.Future[None] = utils.make_done_future()
        self.mock_server_setup_file: pathlib.Path | None = None

    async def telemetry_loop(self) -> None:
        """Publish GIS telemetry until the CSC disconnects or faults.

        Exceptions from telemetry publication are caught, logged, and
        converted to a CSC fault.
        """
        self.log.info("Starting telemetry loop.")
        while True:
            try:
                if self.connected:
                    reply, status_array, status_string = await self.component.update_status()
                    if status_string is None or status_array is None or reply is None:
                        raise RuntimeError("Either status_string, status_array or reply is None.")
                    await self.evt_rawStatus.set_write(status=status_string)
                    await self.fill_out_fields(status_array)
                    await self.publish_new_subsystems(reply)
                    await asyncio.sleep(self.telemetry_interval)
                else:
                    await self.fault(
                        code=ErrorCode.LOST_CONNECTION, report="Unexpectedly disconnected from GIS."
                    )
                    return
            except Exception:
                self.log.exception("Telemetry loop failed.")
                await self.fault(code=ErrorCode.TELEMETRY_FAILED, report="Telemetry loop failed.")
                return

    async def publish_new_subsystems(self, reply: ModbusPDU) -> None:
        """Publish changed raw subsystem register values.

        Parameters
        ----------
        reply : `pymodbus.pdu.ModbusPDU`
            Modbus response containing the latest holding register values.

        Raises
        ------
        AttributeError
            Raised if ``reply`` does not contain ``registers``.
        """
        self.log.debug(f"registers={reply.registers}")
        for index, current_subsystem in enumerate(reply.registers):
            old_subsystem = self.component.system_status[index]
            if current_subsystem != old_subsystem:
                self.component.system_status[index] = current_subsystem
                await self.evt_systemStatus.set_write(index=index, status=current_subsystem)

    async def fill_out_fields(self, status_array: list[list[int]]) -> None:
        """Publish subsystem events from decoded register bits.

        Reserved subsystem entries are skipped.
        For non-reserved subsystems, the corresponding dataclass in
        `lsst.ts.gis.enums` is populated from the subsystem's decoded bits and
        written to the matching SAL event.

        Parameters
        ----------
        status_array : `list` [`list` [`int`]]
            Decoded Modbus register bits, one inner list per subsystem in
            `subsystem_order`.
            Bits are ordered from bit 0 to bit 15 using the Pilz
            least-significant-bit first convention.

        Raises
        ------
        ValueError
            Raised if ``status_array`` does not have one entry per subsystem
            or if a subsystem bit list cannot be mapped to its dataclass.
        AttributeError
            Raised if a subsystem class or SAL event cannot be found.
        """
        if len(status_array) != len(subsystem_order):
            raise ValueError("Length of status_array does not match length of subsystem_order.")
        for status_index, bits in enumerate(status_array):
            subsystem_name = subsystem_order[status_index]
            if "Reserved" in subsystem_name:
                continue

            subsystem_type = getattr(enums, subsystem_name)
            subsystem_data = make_subsystem_data(subsystem_type, bits)
            subsystem_event = getattr(self, f"evt_{subsystem_name}")
            await subsystem_event.set_write(**asdict(subsystem_data))

    @property
    def connected(self) -> bool:
        """Return whether the component is connected.

        Returns
        -------
        connected : `bool`
            `True` if the commander has an active Modbus connection.
        """
        return self.component.connected

    def cleanup_mock_server_setup_file(self) -> None:
        """Remove the temporary simulator JSON file, if one exists."""
        if self.mock_server_setup_file is not None:
            self.mock_server_setup_file.unlink(missing_ok=True)
            self.mock_server_setup_file = None

    async def startup_mock_server(self) -> None:
        """Start the pymodbus simulator for simulation mode.

        A temporary simulator JSON file is created with dynamic Modbus and
        HTTP ports. The component configuration is updated to connect to the
        selected Modbus port.

        Raises
        ------
        RuntimeError
            Raised if the simulator task exits during startup.
        TimeoutError
            Raised if the simulator does not report ready before the startup
            timeout.
        OSError
            Raised if the temporary simulator JSON file cannot be created.
        """
        http_port = get_free_tcp_port()
        modbus_port = get_free_tcp_port()
        ready_task: asyncio.Task[bool] | None = None

        try:
            setup_file = make_simulator_setup_json(SIMULATOR_SETUP_FILE, modbus_port)
            config = self.component.get_config()
            config.tunnel_port = modbus_port
            self.mock_server_setup_file = setup_file
            self.mock_server = ModbusSimulatorServer(
                json_file=setup_file.as_posix(), http_host=LOCALHOST, http_port=http_port
            )
            self.log.info("Starting mock server.")
            self.mock_server_task = asyncio.create_task(self.mock_server.run_forever(only_start=False))
            ready_task = asyncio.create_task(self.mock_server.ready_event.wait())
            done, _ = await asyncio.wait(
                {ready_task, self.mock_server_task},
                timeout=SIMULATOR_START_TIMEOUT,
                return_when=asyncio.FIRST_COMPLETED,
            )

            if self.mock_server_task in done:
                self.mock_server_task.result()

            if ready_task not in done:
                raise TimeoutError("Timed out waiting for mock server to start.")

            ready_task.result()
        except Exception:
            if ready_task is not None and not ready_task.done():
                ready_task.cancel()
            self.mock_server_task.cancel()
            if self.mock_server is not None:
                await self.mock_server.stop()
                self.mock_server = None
            self.cleanup_mock_server_setup_file()
            raise

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

        Raises
        ------
        Exception
            Exceptions from disconnecting or stopping the simulator are
            allowed to propagate to the caller.
        """
        if self.disabled_or_enabled:
            if self.simulation_mode and self.mock_server is None:
                await self.startup_mock_server()
            if not self.connected:
                self.log.info("Connect to the GIS.")
                try:
                    await self.component.connect()
                except Exception:
                    self.log.exception("Failed to connect to the GIS.")
                    await self.fault(code=ErrorCode.CONNECT_FAILED, report="Failed to connect to the GIS.")
                    return
            if self.telemetry_task.done():
                self.telemetry_task = asyncio.create_task(self.telemetry_loop())
        else:
            self.telemetry_task.cancel()
            await self.component.disconnect()
            self.mock_server_task.cancel()
            if self.mock_server is not None:
                await self.mock_server.stop()
                self.mock_server = None
            self.cleanup_mock_server_setup_file()

    async def configure(self, config: GISConfig) -> None:
        """Configure the GIS component.

        Parameters
        ----------
        config : `GISConfig`
            Validated CSC configuration.
        """
        self.telemetry_interval = config.telemetry_interval
        self.component.configure(config)

    @staticmethod
    def get_config_pkg() -> str:
        """Return the name of the configuration repository.

        Returns
        -------
        config_pkg : `str`
            Configuration package name.
        """
        return "ts_config_ocs"

    async def close_tasks(self) -> None:
        """Stop telemetry, simulator, and Modbus connection tasks.

        Raises
        ------
        Exception
            Exceptions from superclass task shutdown are allowed to propagate.
        """
        await self.component.disconnect()
        self.telemetry_task.cancel()
        self.mock_server_task.cancel()
        if self.mock_server is not None:
            await self.mock_server.stop()
            self.mock_server = None
        self.cleanup_mock_server_setup_file()
        await super().close_tasks()
