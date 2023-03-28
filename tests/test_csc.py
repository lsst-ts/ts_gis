import os
import pathlib
import sys
import unittest
from unittest.mock import AsyncMock

import bitarray
from lsst.ts import gis, salobj
from pymodbus.register_read_message import ReadHoldingRegistersResponse

TEST_CONFIG_DIR = pathlib.Path(__file__).parents[1].joinpath("tests", "data", "config")


class GISCscTestCase(salobj.BaseCscTestCase, unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        os.environ["LSST_SITE"] = "gis"
        return super().setUp()

    def basic_make_csc(
        self,
        initial_state,
        config_dir=TEST_CONFIG_DIR,
        simulation_mode=1,
        override="",
    ):
        return gis.GISCsc(
            initial_state=initial_state,
            simulation_mode=simulation_mode,
            override=override,
            config_dir=config_dir,
        )

    async def test_standard_state_transitions(self):
        async with self.make_csc(
            initial_state=salobj.State.STANDBY,
            simulation_mode=1,
            config_dir=TEST_CONFIG_DIR,
        ):
            await self.check_standard_state_transitions(
                enabled_commands=[], override="", timeout=20
            )

    async def test_bin_script(self):
        await self.check_bin_script(
            name="GIS",
            exe_name="run_gis",
            index=None,
        )

    async def test_telemetry(self):
        async with self.make_csc(
            initial_state=salobj.State.ENABLED,
            simulation_mode=1,
            config_dir=TEST_CONFIG_DIR,
        ):
            raw_status = await self.remote.evt_rawStatus.aget(timeout=20)
            assert isinstance(raw_status.status, str)
            assert len(raw_status.status) == 464
            assert raw_status.status == (
                "00000000000000000000000000000000000000000000000000000000000000000000000000000"
                "00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "00000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "0000000000000000000000000000000000000000000000000000000"
            )
            bytes_data = bitarray.bitarray(endian=sys.byteorder)
            bytes_data.extend(raw_status.status)
            assert bytes_data.nbytes == 58
            assert bytes_data.tobytes() == bytearray(
                (
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                )
            )
            assert (
                bytes_data.to01()
                == "0000000000000000000000000000000000000000000000000000000000000000000000000000000"
                + "00000000000000000000000000000000000000000000000000000000000000000000000000000000"
                + "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                + "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                + "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                + "00000000000000000000000000000000000000000000000000000000000000"
            )
            system_status = await self.remote.evt_systemStatus.aget(timeout=20)
            assert system_status.index == 28
            assert system_status.status == 0
            self.csc.component.commander.read = AsyncMock(
                return_value=ReadHoldingRegistersResponse(
                    [
                        232,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                    ]
                )
            )
            raw_status = await self.remote.evt_rawStatus.next(timeout=20, flush=True)
            bytes_data = bitarray.bitarray(endian=sys.byteorder)
            bytes_data.extend(raw_status.status)
            assert bytes_data.tobytes() == bytearray(
                (
                    b"\xe8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                )
            )
            assert bytes_data.to01() == (
                "000101110000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "000000000000000000000000000000000000000000000000000000000000000000000000000000"
                "00000000000000000000000000000000000000000000000000000000000000000000000000"
            )
            new_system_status = await self.remote.evt_systemStatus.next(
                timeout=20, flush=True
            )
            assert new_system_status.index == 0
            assert new_system_status.status == 232


if __name__ == "__main__":
    unittest.main()
