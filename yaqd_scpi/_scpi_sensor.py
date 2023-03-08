__all__ = ["SCPISensor"]

import sys
import asyncio
from typing import Dict, Any, List

import pyvisa
import numpy as np

from yaqd_core import HasMeasureTrigger, IsSensor
from ._scpi_base import SCPIBase


class SCPISensor(HasMeasureTrigger, IsSensor, SCPIBase):
    _kind = "scpi-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._channel_names = list(config["channels"].keys())
        self._channel_units = {k: config["channels"][k]["units"] for k in self._channel_names}

    async def _measure(self):
        out = {}
        for k in self._channel_names:
            query = self._config["channels"][k]["query"]
            self._instrument.write(query)
            try:
                out[k] = float(self._instrument.read())
            except Exception as e:
                self.logger.info(f"error in _measure with key {k}")
                self.logger.error(e)
                out[k] = np.nan
        return out
