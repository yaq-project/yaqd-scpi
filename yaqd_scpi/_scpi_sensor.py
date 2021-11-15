__all__ = ["SCPISensor"]

import sys
import asyncio
from typing import Dict, Any, List

import pyvisa

from yaqd_core import HasMeasureTrigger, IsSensor, IsDaemon


class SCPISensor(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "scpi-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._channel_names = list(config["channels"].keys())
        self._channel_units = {k: config["channels"][k]["units"] for k in self._channel_names}
        if sys.platform.startswith("win32"):
            rm = pyvisa.ResourceManager()  # use ni-visa backend
        else:
            rm = pyvisa.ResourceManager("@py")  # use pyvisa-py backend
        self._instrument = rm.open_resource(config["visa_address"])

    async def _measure(self):
        out = {}
        for k in self._channel_names:
            query = self._config["channels"][k]["query"]
            self._instrument.write(query)
            out[k] = float(self._instrument.read())
        return out
