__all__ = ["GISComponent"]

from logging import Logger
from types import SimpleNamespace

from pymodbus.pdu import ModbusPDU

from .commander import ModbusCommander
from .wizardry import NUMBER_OF_SUBSYSTEMS


class GISComponent:
    """The controller for GIS.

    Parameters
    ----------
    log
        The log reference.
    simulation_mode
        * 0 - real hardware
        * 1 - fake connection

    Attributes
    ----------
    commander : `ModbusCommander` or `None`
        The modbus commander.
    raw_status : `None`
        The bitarray representation of the status.
    system_status : `dict` [`int`, `int`]
        The statuses of the entire GIS.
    log : `logging.Logger`
        The log reference.
    config : `types.SimpleNamespace` or `None`
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
        self.config: None | SimpleNamespace = None
        self.simulation_mode: int = simulation_mode

    @property
    def connected(self) -> bool:
        """Return if the component is connected or not.

        Returns
        -------
        `bool`
            A boolean which determines the connection status of the client.
        """
        if self.commander is not None:
            return self.commander.connected
        else:
            return False

    async def connect(self) -> None:
        """Connect to the commander."""
        assert self.config is not None
        self.commander = ModbusCommander(self.config, self.simulation_mode, log=self.log)
        await self.commander.connect()

    async def disconnect(self) -> None:
        """Disconnect from the commander."""
        if self.commander is not None:
            await self.commander.disconnect()
            self.commander = None

    async def update_status(self) -> tuple[None, None] | tuple[None | ModbusPDU, str]:
        """Update the status of the GIS."""
        assert self.commander is not None
        if self.connected:
            reply = await self.commander.read()
            if reply is not None:
                status_array = self.commander.generate_status_array(reply)
                assert status_array is not None
                status_string = await self.update_raw_status(status_array)
                return reply, status_string
            else:
                return None, None
        else:
            raise RuntimeError("Not connected.")

    async def update_raw_status(self, status_array: list[list[int]]) -> str:
        """Update the raw status event.

        Parameters
        ----------
        status_array : `bytearray`
            The status array that contains the subsystem information.

        Returns
        -------
        status_string: `str`
            The string representation of the status.
        """
        status_string = ""
        for status in status_array:
            status_string += "".join([str(bit) for bit in status]) + " "

        status_string = status_string.rstrip(" ")

        return status_string

    def configure(self, config: SimpleNamespace) -> None:
        """Configure the GIS."""
        self.config = config
