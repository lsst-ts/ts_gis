__all__ = ["ModbusCommander"]

import logging
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

    def __init__(self, config, simulation_mode, log=None) -> None:
        self.modbus_port = config.modbus_port
        self.modbus_host = config.modbus_host
        self.bastion_host = config.bastion_host
        self.bastion_port = config.bastion_port
        self.tunnel_host = config.tunnel_host
        self.tunnel_port = config.tunnel_port
        self.ssh_username = config.ssh_username
        self.ssh_pkey = config.pkey
        self.simulation_mode = simulation_mode
        if log is None:
            self.log = logging.getLogger(type(self).__name__)
        else:
            self.log = log.getChild(type(self).__name__)
        self.client = None

    @property
    def connected(self):
        """Is the commander connected?

        Returns
        -------
        `bool`
            Is the client connected?
        """
        return self.client is not None and self.client.connected

    async def connect(self):
        """Connect to the commander.
        * Opens the sshtunnel if not in simulation mode.
        * Opens the modbus connection to the GIS with sshtunnel.
        """
        if not self.connected:
            if not self.simulation_mode:
                self.tunnel = sshtunnel.open_tunnel(
                    (self.bastion_host, self.bastion_port),
                    ssh_username=self.ssh_username,
                    ssh_pkey=self.ssh_pkey,
                    remote_bind_address=(self.modbus_host, self.modbus_port),
                    local_bind_address=(self.tunnel_host, self.tunnel_port),
                    logger=self.log,
                )
                self.tunnel.start()
                if self.tunnel.tunnel_is_up[(self.tunnel_host, self.tunnel_port)]:
                    self.log.info("Tunnel is up.")
                else:
                    raise RuntimeError("Tunnel is down.")
            self.client = AsyncModbusTcpClient(
                self.tunnel_host, self.tunnel_port, timeout=10
            )
            await self.client.connect()
            if self.client.connected:
                self.log.info("Client connected.")

    async def disconnect(self):
        """Disconnect from the commander.
        sshtunnel is also closed when not in simulation mode.
        """
        if self.connected:
            try:
                self.client.close()
            except Exception:
                pass
            finally:
                self.client = None
            self.log.info("Modbus client is closed.")
            if not self.simulation_mode:
                self.tunnel.close()
                self.log.info("Tunnel is closed.")

    async def read(self):
        """Read the holding registers.

        Returns
        -------
        reply : `pymodbus.register_read_message.ReadHoldingRegistersResponse`
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

    def generate_status_array(self, reply):
        """Generate the system 1's and 0's status of the GIS.

        Parameters
        ----------
        reply : `pymodbus.register_read_message.ReadHoldingRegistersResponse`
            The reply from the modbus server.

        Returns
        -------
        bit_status : `bytearray`
            The 1 and 0's string of each subsystem separated by spaces.
        """
        status_array = bytearray()
        try:
            for data in reply.registers:
                status_array += data.to_bytes(2, sys.byteorder)
            return status_array
        except Exception:
            self.log.exception("Could not generate status array.")
