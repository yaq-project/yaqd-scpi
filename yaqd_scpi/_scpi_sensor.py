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
        while True:
            try:
                query = ";".join([self._config["channels"][k]["query"] for k in self._channel_names])
                if query_error:
                    self.logger.info(str(out))
                response = self._instrument.query(query)
                out = {
                    k: float(s) for k, s in zip(self._channel_names, response.split(";"))
                }
            except Exception as e:
                self.logger.error(e)
                query_error = True
                await asyncio.sleep(0.1)
                continue
            break
        return out
