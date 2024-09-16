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
        query_error = False
        out = {}
        for k in self._channel_names:
            while True:
                try:
                    response = self._instrument.query(self._config["channels"][k]["query"])
                except Exception as e:
                    self.logger.error(f"error in _measure with key {k}")
                    self.logger.error(e)
                    query_error = True
                    await asyncio.sleep(0.1)
                    continue
                out[k] = float(response)
                break
        if query_error:
            self.logger.info(f"afer error, {k} = {str(out)}")
        return out
