__all__ = ["GISComponent"]

from dataclasses import asdict

from . import enums
from .commander import ModbusCommander
from .enums import subsystem_order


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
        self.system_status = dict.fromkeys(range(29), 0)
        self.log = self.csc.log

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
        self.commander = ModbusCommander(
            self.config, self.csc.simulation_mode, log=self.log
        )
        await self.commander.connect()

    async def disconnect(self):
        """Disconnect from the commander."""
        if self.commander is not None:
            await self.commander.disconnect()
            self.commander = None

    async def update_status(self):
        """Update the status of the GIS."""
        if self.connected:
            reply = await self.commander.read()
            if reply is not None:
                status_array = self.commander.generate_status_array(reply)
                status_string = await self.update_raw_status(status_array)
                self.log.debug(f"registers={reply.registers}")
                for index, current_subsystem in enumerate(reply.registers):
                    old_subsystem = self.system_status[index]
                    if current_subsystem != old_subsystem:
                        self.system_status[index] = current_subsystem
                        await self.csc.evt_systemStatus.set_write(
                            index=index, status=current_subsystem
                        )
                await self.fill_out_fields(status_string)
        else:
            raise RuntimeError("Not connected.")

    async def update_raw_status(self, status_array):
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

        await self.csc.evt_rawStatus.set_write(status=status_string)

        return status_string

    async def fill_out_fields(self, statuses):
        """Fill out subsystem event data.

        Iterate through the subsystem 1's and 0's array to publish each
        subsystem's boolean status.
        Some subsystem's have free reserved for future use and the XML has
        a count field greater than one for those blocks.
        The data classes use a tuple field to indicate the appropriate values
        for that XML item.
        Some data classes do not contain any tuples and so can be appended
        to the array as normal.

        Parameters
        ----------
        statuses: `str`
            The string array of 1's and 0's that comprise the status of the
            GIS's subsystems.
        """
        statuses = statuses.split(" ")
        for status_index, status in enumerate(statuses):
            self.log.debug(f"{status=}")
            subsystem_name = getattr(enums, subsystem_order[status_index])
            # For a given string of 1 and 0's, return an array of booleans
            if hasattr(subsystem_name, "tuple_range"):
                tuple_min, tuple_max = subsystem_name.tuple_range()
            else:
                tuple_min = tuple_max = None
            t = tuple()
            status_as_bool = []
            appended_tuple = False
            for bit_index, bit_status in enumerate(status):
                if tuple_max is not None and tuple_min is not None:
                    if bit_index >= tuple_min and bit_index < tuple_max:
                        t += tuple([bool(int(bit_status))])
                    elif bit_index + 1 > tuple_max and not appended_tuple:
                        t += tuple([bool(int(bit_status))])
                        status_as_bool.append(t)
                        appended_tuple = True
                    else:
                        status_as_bool.append(bool(int(bit_status)))
                else:
                    status_as_bool.append(bool(int(bit_status)))
            self.log.debug(f"{status_as_bool=}")
            # Instantiate the data class with the boolean arguments
            subsystem_data = subsystem_name(*status_as_bool)
            subsystem_event = getattr(self.csc, f"evt_{subsystem_order[status_index]}")
            await subsystem_event.set_write(**asdict(subsystem_data))

    def configure(self, config):
        """Configure the GIS."""
        self.config = config
