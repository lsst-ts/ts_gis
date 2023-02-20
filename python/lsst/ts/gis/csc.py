__all__ = ["GISCsc"]

import asyncio

from lsst.ts import salobj, utils
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.server import ModbusTcpServer

from . import __version__
from .component import GISComponent
from .config import CONFIG_SCHEMA


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

    valid_simulation_modes = [0, 1]
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
        self.mock_server = None
        self.component = GISComponent(self)
        self.simulator = None
        self.telemetry_interval = None
        self.telemetry_task = utils.make_done_future()

    async def telemetry_loop(self):
        """Implement the telemetry feed for the GIS."""
        while True:
            try:
                await self.component.update_status()
                await asyncio.sleep(self.telemetry_interval)
            except Exception:
                self.log.exception("Telemetry loop failed.")
                raise

    @property
    def connected(self):
        """Return whether the component is connected."""
        return self.component.connected

    async def handle_summary_state(self):
        if self.disabled_or_enabled:
            if self.simulation_mode and self.mock_server is None:
                child = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [1] * 30))
                context = ModbusServerContext(slaves=child, single=True)
                self.mock_server = ModbusTcpServer(
                    context=context, address=("127.0.0.1", 15020)
                )
                self.log.debug("Starting mock server.")
                self.mock_server_task = asyncio.create_task(
                    self.mock_server.serve_forever()
                )
                await self.mock_server.serving
                self.log.debug("Mock server started.")
            if not self.connected:
                self.component.connect()
            if self.telemetry_task.done() and self.connected:
                self.telemetry_task = asyncio.create_task(self.telemetry_loop())
        else:
            self.telemetry_task.cancel()
            if self.connected:
                self.component.disconnect()
            if self.mock_server is not None:
                await self.mock_server.shutdown()
                self.mock_server_task.cancel()
                self.mock_server = None

    async def configure(self, config):
        """Configure the GIS."""
        self.telemetry_interval = config.telemetry_interval
        self.component.configure(config)

    @staticmethod
    def get_config_pkg():
        return "ts_config_ocs"

    async def close_tasks(self):
        await super().close_tasks()
        self.telemetry_task.cancel()
        self.component.disconnect()
        if self.mock_server is not None:
            await self.mock_server.shutdown()
            self.mock_server = None
