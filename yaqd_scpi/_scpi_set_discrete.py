__all__ = ["SCPISetDiscrete"]

import asyncio
import sys
from typing import Dict, Any, List

import pyvisa

from yaqd_core import IsDiscrete, HasPosition, IsDaemon


class SCPISetDiscrete(IsDiscrete, HasPosition, IsDaemon):
    _kind = "scpi-set-discrete"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self._scpi_command = self._config["scpi_command"]
        self._identifiers_by_position = {k: v for v, k in self._config["identifiers"].items()}
        if sys.platform.startswith("win32"):
            rm = pyvisa.ResourceManager() # use ni-visa backend
        else:
            rm = pyvisa.ResourceManager("@py")  # use pyvisa-py backend
        self._instrument = rm.open_resource(config["visa_address"])

    def _set_position(self, position):
        self._busy = True
        identifier = self._identifiers_by_position[position]
        self._instrument.write(f"{self._scpi_command} {identifier}")

    async def update_state(self):
        while True:
            response = self._instrument.query(f"{self._scpi_command}?").strip()
            self._state["identifier"] = response
            position = self._config["identifiers"][response]
            self._state["position"] = position
            if self._state["position"] == self._state["destination"]:
                self._busy = False
                await asyncio.sleep(0.01)  # fast polling to release busy ASAP during orchestration
            else:
                await asyncio.sleep(0.1)  # slow polling for out-of-band input
