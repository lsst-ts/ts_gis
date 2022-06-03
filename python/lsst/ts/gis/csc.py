__all__ = ["GISCsc"]

import asyncio

from lsst.ts import salobj, utils

from .config import CONFIG_SCHEMA
from .component import GISComponent
from . import __version__


class GISCsc(salobj.ConfigurableCsc):
    """Implement the GIS CSC.

    Parameters
    ----------
    initial_state : `lsst.ts.salobj.State`
    settings_to_apply : `str`
    simulation_mode : `int`
    config_dir : `pathlib.Path`

    Attributes
    ----------
    component : `GISComponent`
    simulator : `None`
    telemetry_task : `asyncio.Future`
    """

    valid_simulation_modes = [0]
    version = __version__

    def __init__(
        self,
        initial_state=salobj.State.STANDBY,
        override=None,
        simulation_mode=False,
        config_dir=None,
    ) -> None:
        super().__init__(
            name="GIS",
            index=None,
            config_schema=CONFIG_SCHEMA,
            initial_state=initial_state,
            override=override,
            simulation_mode=simulation_mode,
            config_dir=config_dir,
        )
        self.component = GISComponent(self)
        self.simulator = None
        self.telemetry_interval = None
        self.telemetry_task = utils.make_done_future()

    async def telemetry_loop(self):
        """Implement the telemetry feed for the GIS."""
        while True:
            await self.component.update_status()
            await asyncio.sleep(self.telemetry_interval)

    @property
    def connected(self):
        """Return whether the component is connected."""
        return self.component.connected

    async def handle_summary_state(self):
        if self.disabled_or_enabled:
            if self.simulation_mode:
                pass
            else:
                pass
            if not self.connected:
                self.component.connect()
            if self.telemetry_task.done():
                self.telemetry_task = asyncio.create_task(self.telemetry_loop())
        else:
            if self.simulator is not None:
                await self.simulator.close()
                self.simulator = None
            self.component.disconnect()
            self.telemetry_task.cancel()

    async def configure(self, config):
        """Configure the GIS."""
        self.telemetry_interval = config.telemetry_interval
        self.component.configure(config)

    @staticmethod
    def get_config_pkg():
        return "ts_config_ocs"