import json
import logging
import pathlib
import unittest
from types import SimpleNamespace

from lsst.ts.gis.commander import ModbusCommander
from lsst.ts.gis.enums import subsystem_order
from lsst.ts.gis.wizardry import (
    BITS_PER_REGISTER,
    EXPECTED_LENGTH_OF_STATUS,
    MAX_UINT16,
    MODBUS_START_ADDRESS,
    NUMBER_OF_SPACES,
    NUMBER_OF_SUBSYSTEMS,
)

BASTION_PORT = 22
MODBUS_PORT = 502
SIMULATOR_MODBUS_PORT = 15020
TEST_HOST = "127.0.0.1"
SETUP_JSON = pathlib.Path(__file__).parents[1] / "python" / "lsst" / "ts" / "gis" / "data" / "setup.json"


def make_config() -> SimpleNamespace:
    return SimpleNamespace(
        modbus_host=TEST_HOST,
        modbus_port=MODBUS_PORT,
        bastion_host=TEST_HOST,
        bastion_port=BASTION_PORT,
        tunnel_host=TEST_HOST,
        tunnel_port=SIMULATOR_MODBUS_PORT,
        ssh_username="gis-bastion",
        pkey="~/.ssh/id_gis_bastion",
    )


class RegisterReply:
    def __init__(self, registers: list[int]) -> None:
        self.registers = registers


class FakeClient:
    def __init__(self, connected: bool = True, reply: RegisterReply | None = None) -> None:
        self.connected = connected
        self.closed = False
        self.reply = reply

    def close(self) -> None:
        self.closed = True

    async def read_holding_registers(self, address: int, count: int) -> RegisterReply:
        assert address == MODBUS_START_ADDRESS
        assert count == NUMBER_OF_SUBSYSTEMS
        if self.reply is None:
            raise RuntimeError("No reply configured.")
        return self.reply


class FakeTunnel:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


class ModbusCommanderTestCase(unittest.IsolatedAsyncioTestCase):
    def make_commander(self, simulation_mode: int = 1) -> ModbusCommander:
        return ModbusCommander(
            config=make_config(),
            simulation_mode=simulation_mode,
            log=logging.getLogger(type(self).__name__),
        )

    def test_register_map_consistency(self) -> None:
        setup = json.loads(SETUP_JSON.read_text())
        register_range = setup["device_list"]["device"]["uint16"][0]["addr"]

        self.assertEqual(len(subsystem_order), NUMBER_OF_SUBSYSTEMS)
        self.assertEqual(NUMBER_OF_SPACES, NUMBER_OF_SUBSYSTEMS - 1)
        self.assertEqual(
            EXPECTED_LENGTH_OF_STATUS,
            NUMBER_OF_SUBSYSTEMS * BITS_PER_REGISTER + NUMBER_OF_SPACES,
        )
        self.assertEqual(setup["device_list"]["device"]["setup"]["hr size"], NUMBER_OF_SUBSYSTEMS)
        self.assertEqual(register_range, [0, NUMBER_OF_SUBSYSTEMS - 1])

    def test_generate_status_array_validates_reply(self) -> None:
        commander = self.make_commander()

        self.assertIsNone(commander.generate_status_array(SimpleNamespace()))
        self.assertIsNone(commander.generate_status_array(RegisterReply([0] * (NUMBER_OF_SUBSYSTEMS - 1))))
        self.assertIsNone(
            commander.generate_status_array(RegisterReply([MAX_UINT16 + 1] * NUMBER_OF_SUBSYSTEMS))
        )

        status_array = commander.generate_status_array(
            RegisterReply([0, 1, MAX_UINT16] + [0] * (NUMBER_OF_SUBSYSTEMS - 3))
        )

        self.assertIsNotNone(status_array)
        self.assertEqual(len(status_array), NUMBER_OF_SUBSYSTEMS)
        self.assertEqual(status_array[0], [0] * BITS_PER_REGISTER)
        self.assertEqual(status_array[1], [1] + [0] * (BITS_PER_REGISTER - 1))
        self.assertEqual(status_array[2], [1] * BITS_PER_REGISTER)

    async def test_read_uses_connected_client(self) -> None:
        commander = self.make_commander()
        expected_reply = RegisterReply([0] * NUMBER_OF_SUBSYSTEMS)
        commander.client = FakeClient(reply=expected_reply)  # type: ignore[assignment]

        reply = await commander.read()

        self.assertIs(reply, expected_reply)

    async def test_read_raises_without_connected_client(self) -> None:
        commander = self.make_commander()

        with self.assertRaisesRegex(RuntimeError, "not configured"):
            await commander.read()

        commander.client = FakeClient(connected=False)  # type: ignore[assignment]
        with self.assertRaisesRegex(RuntimeError, "not connected"):
            await commander.read()

    async def test_disconnect_closes_client_and_tunnel(self) -> None:
        commander = self.make_commander(simulation_mode=0)
        client = FakeClient()
        tunnel = FakeTunnel()
        commander.client = client  # type: ignore[assignment]
        commander.tunnel = tunnel  # type: ignore[assignment]

        await commander.disconnect()

        self.assertTrue(client.closed)
        self.assertTrue(tunnel.closed)
        self.assertIsNone(commander.client)
        self.assertIsNone(commander.tunnel)
