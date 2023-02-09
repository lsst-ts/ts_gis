__all__ = ["ModbusCommander"]

import sys

from pymodbus.client import ModbusTcpClient


class ModbusCommander:
    """Wrapper around the modbus client.

    Parameters
    ----------
    host : `str`
    port : `int`

    Attributes
    ----------
    port : `int`
    host : `str`
    client : `pymodbus.client.sync.ModbusTcpClient`
    """

    def __init__(self, host, port) -> None:
        self.port = port
        self.host = host
        self.client = None

    @property
    def connected(self):
        """Is the commander connected?

        Returns
        -------
        `bool`
        """
        if self.client is None or not self.client.is_socket_open:
            return False
        else:
            return True

    def connect(self):
        """Connect to the commander."""
        if not self.connected:
            self.client = ModbusTcpClient(self.host, self.port)
            self.client.connect()

    def disconnect(self):
        """Disconnect from the commander."""
        if self.connected:
            self.client = None

    def read(self):
        """Read the holding registers.

        Returns
        -------
        reply : `HoldRegisterReply`
            The reply from the modbus server.

        Raises
        ------
        `RuntimeError`
            Raised when the client is not connected to the modbus server.
        """
        if self.connected:
            reply = self.client.read_holding_registers(0, 29)
            return reply
        else:
            raise RuntimeError("Commander is not connected.")

    def get_raw_string(self, reply):
        """Generate the raw system byte status of the GIS.

        Parameters
        ----------
        reply : `HoldRegisterReply`
            The reply from the modbus server.

        Returns
        -------
        raw_status : `bytearray`
            The unfiltered response of the reply in a byte array.
        """
        raw_status = bytearray()
        for data in reply.registers:
            raw_status += data.to_bytes(2, sys.byteorder)
        return raw_status
