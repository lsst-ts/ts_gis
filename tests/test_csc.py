import os
import pathlib
import unittest

import pytest
from lsst.ts import gis, salobj

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

    @pytest.mark.skip("Update client to async.")
    async def test_telemetry(self):
        async with self.make_csc(
            initial_state=salobj.State.ENABLED,
            simulation_mode=1,
            config_dir=TEST_CONFIG_DIR,
        ):
            await self.remote.evt_rawStatus.aget(timeout=20)
            system_status = await self.remote.evt_systemStatus.aget(timeout=20)
            assert system_status.index == 28
            assert system_status.status == 1


if __name__ == "__main__":
    unittest.main()
