__all__ = ["ModbusCommander"]

import logging

import sshtunnel
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ModbusPDU

from .config import GISConfig
from .wizardry import BITS_PER_REGISTER, MAX_UINT16, MODBUS_START_ADDRESS, NUMBER_OF_SUBSYSTEMS


class ModbusCommander:
    """Manage Modbus client and optional SSH tunnel connections.

    Parameters
    ----------
    config : `GISConfig`
        Validated GIS configuration.
    simulation_mode : `int`
        Simulation mode. Use 0 for real hardware and 1 for a simulated
        Modbus connection.
    log : `logging.Logger` or `None`, optional
        Parent logger. If `None`, a module logger is created.

    Attributes
    ----------
    modbus_port : `int`
        The port for the modbus server.
    modbus_host : `str`
        The hostname of the modbus server.
    bastion_host : `str`
        The hostname of the bastion used for the SSH tunnel.
    bastion_port : `int`
        The port of the bastion host.
    tunnel_host : `str`
        The local host used for the SSH tunnel.
    tunnel_port : `int`
        The local port used for the SSH tunnel.
    ssh_username : `str`
        The SSH username for the tunnel connection.
    ssh_pkey : `str`
        The private key path or value for SSH authentication.
    simulation_mode : `int`
        Whether the commander is running in simulation mode.
    log : `logging.Logger`
        The logger used by the commander.
    client : `pymodbus.client.AsyncModbusTcpClient` or `None`
        The modbus TCP client.
    tunnel : `sshtunnel.SSHTunnelForwarder` or `None`
        The SSH tunnel forwarder.
    connected : `bool`
        Whether the commander is connected.
    """

    def __init__(self, config: GISConfig, simulation_mode: int, log: None | logging.Logger = None) -> None:
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
        """Return whether the Modbus client is connected.

        Returns
        -------
        connected : `bool`
            `True` if the Modbus client exists and reports that it is
            connected.
        """
        return self.client is not None and self.client.connected

    def get_client(self) -> AsyncModbusTcpClient:
        """Return the connected Modbus client.

        Returns
        -------
        client : `pymodbus.client.AsyncModbusTcpClient`
            Connected Modbus TCP client.

        Raises
        ------
        RuntimeError
            Raised if the client is missing or disconnected.
        """
        client = self.client
        if client is None:
            raise RuntimeError("Modbus client is not configured.")
        if not client.connected:
            raise RuntimeError("Modbus client is not connected.")
        return client

    async def connect(self) -> None:
        """Connect to the GIS Modbus server.

        In real-hardware mode this starts an SSH tunnel first, then connects
        the Modbus client through the tunnel. In simulation mode it connects
        directly to the configured local simulator endpoint.

        Raises
        ------
        RuntimeError
            Raised if the SSH tunnel or Modbus client fails to connect.
        Exception
            Exceptions raised during setup are allowed to propagate after
            partial resources are cleaned up.
        """
        if not self.connected:
            try:
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
                else:
                    raise RuntimeError("Modbus client failed to connect.")
            except Exception:
                await self.disconnect()
                raise

    async def disconnect(self) -> None:
        """Close the Modbus client and optional SSH tunnel.

        Cleanup exceptions are logged and suppressed so disconnect can finish
        releasing any remaining resources.
        """
        if self.client is not None:
            try:
                self.client.close()
            except Exception:
                self.log.exception("Failed to close Modbus client.")
            finally:
                self.client = None
            self.log.info("Modbus client is closed.")

        if not self.simulation_mode and self.tunnel is not None:
            try:
                self.tunnel.close()
            except Exception:
                self.log.exception("Failed to close SSH tunnel.")
            finally:
                self.tunnel = None
                self.log.info("Tunnel is closed.")

    async def read(self) -> None | ModbusPDU:
        """Read the holding registers.

        Returns
        -------
        reply : `pymodbus.pdu.ModbusPDU` or `None`
            Modbus response from the server. `None` if the read returns a
            `pymodbus.exceptions.ModbusIOException`.

        Raises
        ------
        RuntimeError
            Raised if the client is missing or disconnected.
        """
        client = self.get_client()
        reply = await client.read_holding_registers(address=MODBUS_START_ADDRESS, count=NUMBER_OF_SUBSYSTEMS)
        if isinstance(reply, ModbusIOException):
            self.log.error(f"Modbus read failed: {reply}")
            return None
        return reply

    def generate_status_array(self, reply: ModbusPDU) -> None | list[list[int]]:
        """Decode Modbus holding registers into subsystem bit arrays.

        Parameters
        ----------
        reply : `pymodbus.pdu.ModbusPDU`
            Modbus response containing holding register values.

        Returns
        -------
        status_array : `list` [`list` [`int`]] or `None`
            Register bits in Pilz least-significant-bit first order, one
            inner list per subsystem. `None` if the reply is malformed.
        """
        status_array: list[list[int]] = []
        try:
            if not hasattr(reply, "registers"):
                self.log.error("Reply does not contain registers.")
                return None
            registers = reply.registers
            if len(registers) != NUMBER_OF_SUBSYSTEMS:
                self.log.error(f"Expected {NUMBER_OF_SUBSYSTEMS} registers, got {len(registers)}.")
                return None
            for data in registers:
                register = int(data)
                if register < 0 or register > MAX_UINT16:
                    self.log.error(f"Register value {register} is outside uint16 range.")
                    return None
                # According to Pilz PNOZmulti Modbus convention, we use LSB
                # (least significant bit) ordering.
                # source: https://cdn.logic-control.com/docs/pilz-safety/Manuals/PNOZmulti_Com_Interface_Op_Man_1001154-EN-13.pdf
                status_array.append([(register >> bit) & 1 for bit in range(BITS_PER_REGISTER)])
            return status_array
        except Exception:
            self.log.exception("Could not generate status array.")
            return None
