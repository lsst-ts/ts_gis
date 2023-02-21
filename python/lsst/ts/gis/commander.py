__all__ = ["ModbusCommander"]

import logging
import os
import sys

import sshtunnel
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException


class ModbusCommander:
    """Wrapper around the modbus client.

    Parameters
    ----------
    config : `types.SimpleNamespace`
        The configuration.
    simulation_mode : `int`
        Is the GIS simulated?

    Attributes
    ----------
    modbus_port : `int`
        The modbus port.
    modbus_host : `str`
        The modbus host.
    bastion_host : `str`
        The bastion server hostname.
    bastion_port : `int`
        The bastion server's ssh port.
    tunnel_host : `str`
        The local bind's host.
        Usually localhost.
    tunnel_port : `int`
        The local bind's port.
    client : `pymodbus.client.AsyncModbusTcpClient`
        The pymodbus async client.
    """

    def __init__(self, config, simulation_mode) -> None:
        self.modbus_port = config.modbus_port
        self.modbus_host = config.modbus_host
        self.bastion_host = config.bastion_host
        self.bastion_port = config.bastion_port
        self.tunnel_host = config.tunnel_host
        self.tunnel_port = config.tunnel_port
        self.simulation_mode = simulation_mode
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
            if not self.simulation_mode:
                self.tunnel = sshtunnel.open_tunnel(
                    (self.bastion_host, self.bastion_port),
                    ssh_username="saluser",
                    password=os.environ["GIS_PASSWORD"],
                    remote_bind_address=(self.modbus_host, self.modbus_port),
                    local_bind_address=(self.tunnel_host, self.tunnel_port),
                )
                self.log.info("Tunnel is up.")
            self.client = AsyncModbusTcpClient(
                self.tunnel_host, self.tunnel_port, timeout=10
            )
            await self.client.connect()
            self.log.info("Client connected.")

    async def disconnect(self):
        """Disconnect from the commander."""
        if self.connected:
            await self.client.close()
            self.log.info("Modbus client is closed.")
            self.client = None
            if not self.simulation_mode:
                self.tunnel.close()
                self.log.info("Tunnel is closed.")

    async def read(self):
        """Read the holding registers.

        Returns
        -------
        reply : `pymodbus.register_read_message.ReadHoldingRegistersResponse` or `pymodbus.exceptions.ModbusIOException` # noqa
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
        reply : `pymodbus.register_read_message.ReadHoldingRegistersResponse`
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
