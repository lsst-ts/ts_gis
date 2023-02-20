__all__ = ["GISComponent"]

import itertools
import logging

from .commander import ModbusCommander


class GISComponent:
    """The controller for GIS.

    Parameters
    ----------
    csc : `GISCsc`
        The GIS CSC.

    Attributes
    ----------
    commander : `ModbusCommander`
        The modbus commander.
    csc : `GISCsc`
        The GIS CSC.
    raw_status : `bytearray`
        The bitarray representation of the status.
    system_status : `list` of `int`
        The statuses of the entire GIS.
    """

    def __init__(self, csc) -> None:
        self.commander = None
        self.csc = csc
        self.raw_status = None
        self.system_status = []
        self.log = logging.getLogger(__name__)

    @property
    def connected(self):
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

    async def connect(self):
        """Connect to the commander."""
        self.commander = ModbusCommander(self.config.host, self.config.port)
        await self.commander.connect()

    async def disconnect(self):
        """Disconnect from the commander."""
        if self.commander is not None:
            await self.commander.disconnect()
            self.commander = None

    async def update_status(self):
        """Update the status of the GIS."""
        reply = await self.commander.read()
        if reply is not None:
            raw_status = self.commander.get_raw_string(reply)
            if self.raw_status != raw_status:
                await self.csc.evt_rawStatus.set_write(status=raw_status)
            self.raw_status = raw_status
            for index, (current_subsystem, old_subsystem) in enumerate(
                itertools.zip_longest(
                    reply.registers, self.system_status, fillvalue=None
                )
            ):
                if current_subsystem != old_subsystem:
                    await self.csc.evt_systemStatus.set_write(
                        index=index, status=current_subsystem
                    )
            self.system_status = reply.registers

    def configure(self, config):
        """Configure the GIS."""
        self.config = config
