__all__ = ["SCPIBase"]

import pyvisa
import sys

from yaqd_core import IsDaemon


class SCPIBase(IsDaemon):
    _kind = "scpi-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        if sys.platform.startswith("win32"):
            self.rm = pyvisa.ResourceManager()  # use ni-visa backend
        else:
            self.rm = pyvisa.ResourceManager("@py")  # use pyvisa-py backend
        self._loop.create_task(self.connect_instrument(config["visa_address"], timeout=1000))

    async def connect_instrument(self, *args, **kwargs):
        with self.rm.open_resource(*args, **kwargs) as instr:
            self._instrument: pyvisa.Resource = instr
            await asyncio.sleep(1)

    def direct_scpi_write(self, command: str):
        self._instrument.write(command)
