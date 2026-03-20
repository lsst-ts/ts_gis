__all__ = ["ModbusCommander"]

import logging
from types import SimpleNamespace

import sshtunnel
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ModbusPDU


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

    def __init__(
        self, config: SimpleNamespace, simulation_mode: int, log: None | logging.Logger = None
    ) -> None:
        self.modbus_port: int = config.modbus_port
        self.modbus_host: str = config.modbus_host
        self.bastion_host: str = config.bastion_host
        self.bastion_port: int = config.bastion_port
        self.tunnel_host: str = config.tunnel_host
        self.tunnel_port: int = config.tunnel_port
        self.ssh_username: str = config.ssh_username
        self.ssh_pkey: str = config.pkey
        self.simulation_mode: int = simulation_mode
        if log is None:
            self.log = logging.getLogger(type(self).__name__)
        else:
            self.log = log.getChild(type(self).__name__)
        self.client: None | AsyncModbusTcpClient = None
        self.tunnel: None | sshtunnel.SSHTunnelForwarder = None

    @property
    def connected(self) -> bool:
        """Is the commander connected?

        Returns
        -------
        `bool`
            Is the client connected?
        """
        return self.client is not None and self.client.connected

    async def connect(self) -> None:
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
            self.client = AsyncModbusTcpClient(host=self.tunnel_host, port=self.tunnel_port, timeout=10)
            await self.client.connect()
            if self.client.connected:
                self.log.info("Client connected.")

    async def disconnect(self) -> None:
        """Disconnect from the commander.
        sshtunnel is also closed when not in simulation mode.
        """
        if self.connected:
            try:
                assert self.client is not None
                self.client.close()
            except Exception:
                pass
            finally:
                self.client = None
            self.log.info("Modbus client is closed.")
            if not self.simulation_mode:
                assert self.tunnel is not None
                self.tunnel.close()
                self.log.info("Tunnel is closed.")

    async def read(self) -> None | ModbusPDU:
        """Read the holding registers.

        Returns
        -------
        reply : `pymodbus.pdu.ModbusPDU`
            The reply from the modbus server.
            Can also be a ModbusIOException.

        Raises
        ------
        `RuntimeError`
            Raised when the client is not connected to the modbus server.
        """
        assert self.client is not None
        if self.connected:
            reply = await self.client.read_holding_registers(address=0, count=33)
            if not isinstance(reply, ModbusIOException):
                return reply
            else:
                self.log.exception(f"{reply.string}")
                return None
        else:
            raise RuntimeError("Commander is not connected.")

    def generate_status_array(self, reply: ModbusPDU) -> None | list[list[int]]:
        """Generate the system 1's and 0's status of the GIS.

        Parameters
        ----------
        reply : `pymodbus.pdu.ModbusPDU`
            The reply from the modbus server.

        Returns
        -------
        bit_status : `bytearray`
            The 1 and 0's string of each subsystem separated by spaces.
        """
        status_array: list[list[int]] = []
        try:
            for data in reply.registers:
                status_array.append([int(x) for x in f"{data:016b}"])
            return status_array
        except Exception:
            self.log.exception("Could not generate status array.")
            return None
