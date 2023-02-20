__all__ = ["ModbusCommander"]

import logging
import sys

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException


class ModbusCommander:
    """Wrapper around the modbus client.

    Parameters
    ----------
    host : `str`
        The modbus host to connect to.
    port : `int`
        The modbus port to connect to.

    Attributes
    ----------
    port : `int`
        The modbus port.
    host : `str`
        The modbus host.
    client : `pymodbus.client.AsyncModbusTcpClient`
        The pymodbus async client.
    """

    def __init__(self, host, port) -> None:
        self.port = port
        self.host = host
        self.log = logging.getLogger(__name__)
        self.client = None

    @property
    def connected(self):
        """Is the commander connected?

        Returns
        -------
        `bool`
            Is the client connected?
        """
        if self.client is None or not self.client.connected:
            return False
        else:
            return True

    async def connect(self):
        """Connect to the commander."""
        if not self.connected:
            self.client = AsyncModbusTcpClient(self.host, self.port, timeout=10)
            await self.client.connect()
            self.log.info("Client connected.")

    async def disconnect(self):
        """Disconnect from the commander."""
        if self.connected:
            await self.client.close()
            self.client = None

    async def read(self):
        """Read the holding registers.

        Returns
        -------
        reply : `ReadHoldingRegistersResponse` or `ModbusIOException`
            The reply from the modbus server.
            Can also be a ModbusIOException.

        Raises
        ------
        `RuntimeError`
            Raised when the client is not connected to the modbus server.
        """
        if self.connected:
            reply = await self.client.read_holding_registers(0, 29)
            if not isinstance(reply, ModbusIOException):
                return reply
            else:
                self.log.exception(f"{reply.string}")
        else:
            raise RuntimeError("Commander is not connected.")

    def get_raw_string(self, reply):
        """Generate the raw system byte status of the GIS.

        Parameters
        ----------
        reply : `ReadHoldingRegisterResponse`
            The reply from the modbus server.

        Returns
        -------
        raw_status : `bytearray`
            The unfiltered response of the reply in a byte array.
        """
        raw_status = bytearray()
        try:
            for data in reply.registers:
                raw_status += data.to_bytes(2, sys.byteorder)
            return raw_status
        except Exception:
            self.log.exception("Something went wrong.")
