__all__ = ["GISComponent"]

from logging import Logger

from pymodbus.pdu import ModbusPDU

from .commander import ModbusCommander
from .config import GISConfig
from .wizardry import NUMBER_OF_SUBSYSTEMS


class GISComponent:
    """Coordinate Modbus communication and GIS status formatting.

    Parameters
    ----------
    log : `logging.Logger`
        Logger used by the component and commander.
    simulation_mode : `int`, optional
        Simulation mode. Use 0 for real hardware and 1 for a simulated
        Modbus connection.

    Attributes
    ----------
    commander : `ModbusCommander` or `None`
        The modbus commander.
    raw_status : `None`
        Placeholder for raw status state.
    system_status : `dict` [`int`, `int`]
        The statuses of the entire GIS.
    log : `logging.Logger`
        The log reference.
    config : `GISConfig` or `None`
        The configuration.
    simulation_mode : `int`
        The simulation mode.
    connected : `bool`
        Whether the component is connected.
    """

    def __init__(self, log: Logger, simulation_mode: int = 0) -> None:
        self.commander: None | ModbusCommander = None
        self.raw_status: None = None
        self.system_status: dict[int, int] = dict.fromkeys(range(NUMBER_OF_SUBSYSTEMS), 0)
        self.log: Logger = log
        self.config: None | GISConfig = None
        self.simulation_mode: int = simulation_mode

    def get_config(self) -> GISConfig:
        """Return the configured GIS configuration.

        Returns
        -------
        config : `GISConfig`
            Current component configuration.

        Raises
        ------
        RuntimeError
            Raised if the component has not been configured.
        """
        if self.config is None:
            raise RuntimeError("GIS component has not been configured.")
        return self.config

    @property
    def connected(self) -> bool:
        """Return whether the component is connected.

        Returns
        -------
        connected : `bool`
            `True` if a commander exists and its Modbus client is connected.
        """
        if self.commander is not None:
            return self.commander.connected
        else:
            return False

    async def connect(self) -> None:
        """Create and connect the Modbus commander.

        Raises
        ------
        RuntimeError
            Raised if the component has not been configured.
        Exception
            Exceptions from the commander connection attempt are allowed to
            propagate to the caller.
        """
        config = self.get_config()
        self.commander = ModbusCommander(config, self.simulation_mode, log=self.log)
        await self.commander.connect()

    async def disconnect(self) -> None:
        """Disconnect and discard the Modbus commander.

        Raises
        ------
        Exception
            Exceptions from commander cleanup are allowed to propagate to the
            caller.
        """
        if self.commander is not None:
            await self.commander.disconnect()
            self.commander = None

    def get_commander(self) -> ModbusCommander:
        """Return the connected Modbus commander.

        Returns
        -------
        commander : `ModbusCommander`
            Connected Modbus commander.

        Raises
        ------
        RuntimeError
            Raised if the commander is missing or not connected.
        """
        commander = self.commander
        if commander is None:
            raise RuntimeError("Commander is not configured.")
        if not commander.connected:
            raise RuntimeError("Commander is not connected.")
        return commander

    async def update_status(self) -> tuple[ModbusPDU | None, list[list[int]] | None, str | None]:
        """Read and decode the current GIS status.

        Returns
        -------
        reply : `pymodbus.pdu.ModbusPDU` or `None`
            Raw Modbus response. `None` if the read failed.
        status_array : `list` [`list` [`int`]] or `None`
            Decoded register bits, one inner list per subsystem. `None` if
            the read failed.
        status_string : `str` or `None`
            Raw status event string. `None` if the read failed.

        Raises
        ------
        RuntimeError
            Raised if the commander is missing, disconnected, or the response
            cannot be decoded into a status array.
        """
        commander = self.get_commander()

        reply = await commander.read()
        if reply is None:
            return None, None, None

        status_array = commander.generate_status_array(reply)
        if status_array is None:
            raise RuntimeError("Could not generate status array.")

        status_string = await self.update_raw_status(status_array)
        return reply, status_array, status_string

    async def update_raw_status(self, status_array: list[list[int]]) -> str:
        """Format decoded status bits for the raw status event.

        Parameters
        ----------
        status_array : `list` [`list` [`int`]]
            Decoded register bits, one inner list per subsystem.

        Returns
        -------
        status_string : `str`
            Space-separated bit strings for all subsystems.
        """
        return " ".join("".join(str(bit) for bit in status) for status in status_array)

    def configure(self, config: GISConfig) -> None:
        """Store the component configuration.

        Parameters
        ----------
        config : `GISConfig`
            Validated GIS configuration.
        """
        self.config = config
