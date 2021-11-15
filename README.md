# yaqd-scpi

[![PyPI](https://img.shields.io/pypi/v/yaqd-scpi)](https://pypi.org/project/yaqd-scpi)
[![Conda](https://img.shields.io/conda/vn/conda-forge/yaqd-scpi)](https://anaconda.org/conda-forge/yaqd-scpi)
[![yaq](https://img.shields.io/badge/framework-yaq-orange)](https://yaq.fyi/)
[![black](https://img.shields.io/badge/code--style-black-black)](https://black.readthedocs.io/)
[![ver](https://img.shields.io/badge/calver-YYYY.0M.MICRO-blue)](https://calver.org/)
[![log](https://img.shields.io/badge/change-log-informational)](https://gitlab.com/yaq/yaqd-scpi/-/blob/main/CHANGELOG.md)

yaq daemons for SCPI hardware.
This package contains a few very generic daemons for interacting with the SCPI bus from yaq.
The generic approach works well for many simple applications, but more complex hardware interaction may require a more hardware-specific daemon.

## scpi-sensor

[`scpi-sensor`](https://yaq.fyi/daemons/scpi-sensor) allows yaq users to treat one or more scalar queries as a standard yaq sensor.
Multiple queries are treated as multiple channels.
Users can define channel names and units via config.
An example config follows:

```toml
[rigol]
port = 39999
visa_address = "TCPIP0::128.104.68.66::INSTR"
[rigol.channels]
[rigol.channels.trigger_level]
query = "TRIG:EDGE:LEV?"
units = "V"
[rigol.channels.time_offset]
query = "TIM:MAIN:OFFS?"
units = "s"
```

## scpi-set-continuous

[`scpi-set-continuous`](https://yaq.fyi/daemons/scpi-set-continuous) allows yaq users to address a single scalar settable.
Limits and units can be provided via config.
An example config follows:

```toml
[rigol_ch1_freq]
port = 39998
visa_address = "TCPIP0::128.104.68.66::INSTR"
limits = [0.1, 25e9]
scpi_command = "SOUR1:FREQ"

[rigol_ch2_freq]
port = 39999
visa_address = "TCPIP0::128.104.68.66::INSTR"
limits = [0.1, 25e9]
scpi_command = "SOUR1:FREQ"
```

## scpi-set-discrete

[`scpi-set-discrete`](https://yaq.fyi/daemons/scpi-set-discrete) allows yaq users to address a single non-scalar settable according to user-friendly names.
Identifiers must be provided via config.
An example config follows:

```toml
[rigol_ch1_func]
port = 39999
visa_address = "TCPIP0::128.104.68.66::INSTR"
scpi_command = "SOUR1:FUNC"
identifiers = {"SIN"=0, "SQU"=1, "RAMP"=2, "PULS"=3, "NOIS"=4, "DC"=5}
```