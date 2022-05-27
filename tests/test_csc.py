import unittest
import pathlib
import os

from lsst.ts import salobj, gis


TEST_CONFIG_DIR = pathlib.Path(__file__).parents[1].joinpath("tests", "data", "config")


class GISCscTestCase(unittest.IsolatedAsyncioTestCase, salobj.BaseCscTestCase):
    def setUp(self) -> None:
        os.environ["LSST_SITE"] = "gis"
        return super().setUp()

    def basic_make_csc(
        self,
        initial_state,
        config_dir=TEST_CONFIG_DIR,
        simulation_mode=0,
        override="",
    ):
        return gis.GISCsc(
            initial_state=initial_state,
            simulation_mode=simulation_mode,
            override=override,
            config_dir=config_dir,
        )

    async def test_standard_state_transitions(self):
        async with self.make_csc(initial_state=salobj.State.STANDBY):
            await self.check_standard_state_transitions(
                enabled_commands=[], override=""
            )

    async def test_bin_script(self):
        await self.check_bin_script(
            name="GIS",
            exe_name="run_gis_csc.py",
            index=None,
        )


if __name__ == "__main__":
    unittest.main()
