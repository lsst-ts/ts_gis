__all__ = [
    "BITS_PER_REGISTER",
    "EXPECTED_LENGTH_OF_STATUS",
    "MAX_UINT16",
    "MODBUS_START_ADDRESS",
    "NUMBER_OF_SPACES",
    "NUMBER_OF_SUBSYSTEMS",
]

BITS_PER_REGISTER = 16
"""Number of bits in one Modbus register."""
MAX_UINT16 = 0xFFFF
"""Maximum unsigned 16-bit register value."""
MODBUS_START_ADDRESS = 0
"""First Modbus holding register address to read."""

NUMBER_OF_SUBSYSTEMS = 35
"""Number of subsystems."""
NUMBER_OF_SPACES = 34
"""Number of spaces between subsystem string."""
EXPECTED_LENGTH_OF_STATUS = NUMBER_OF_SUBSYSTEMS * BITS_PER_REGISTER + NUMBER_OF_SPACES
"""Expected length of system status."""
