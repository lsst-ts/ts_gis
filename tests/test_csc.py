import unittest

from lsst.ts import salobj, gis


class GISCscTestCase(unittest.IsolatedAsyncioTestCase, salobj.BaseCscTestCase):
    def basic_make_csc(
        self,
        initial_state,
        config_dir=None,
        simulation_mode=0,
        settings_to_apply="",
    ):
        return gis.GISCsc(
            initial_state=initial_state,
            simulation_mode=simulation_mode,
            settings_to_apply=settings_to_apply,
            config_dir=config_dir,
        )

    async def test_standard_state_transitions(self):
        async with self.make_csc(initial_state=salobj.State.STANDBY):
            await self.check_standard_state_transitions(
                enabled_commands=[], settingsToApply=""
            )

    async def test_bin_script(self):
        await self.check_bin_script(
            name="GIS",
            exe_name="run_gis_csc.py",
            index=None,
        )


if __name__ == "__main__":
    unittest.main()
