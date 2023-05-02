import os
import pathlib
import unittest
from unittest.mock import AsyncMock

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
            assert len(raw_status.status) == 521
            assert raw_status.status == " ".join(("00000000",) * 58)
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
            new_system_status = await self.remote.evt_systemStatus.next(
                timeout=20, flush=True
            )
            assert new_system_status.index == 0
            assert new_system_status.status == 232


if __name__ == "__main__":
    unittest.main()
