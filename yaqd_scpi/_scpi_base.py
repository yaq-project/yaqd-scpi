__all__ = ["SCPIBase"]

import pyvisa

from yaqd_core import IsDaemon


class SCPIBase(IsDaemon):
    _kind = "scpi-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        if sys.platform.startswith("win32"):
            rm = pyvisa.ResourceManager()  # use ni-visa backend
        else:
            rm = pyvisa.ResourceManager("@py")  # use pyvisa-py backend
        self._instrument = rm.open_resource(config["visa_address"])

    def direct_scpi_write(command: str):
        self._instrument.write(command)

    def close(self):
        if self._instrument is None:
            return
        self.instrument.close()
