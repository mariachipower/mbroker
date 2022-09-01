Install:

Command line network broker client for Mariachi Power Electronics Industrial Controllers

pip install -U pip setuptools

pip install .


Usage:

[3] → mbroker
Usage: mbroker [OPTIONS] COMMAND [ARGS]...

  This script showcases different terminal UI helpers in Click.

Options:
  --help  Show this message and exit.

Commands:
  add      Add Mariachi devices.
  init     Creates config.json + dirs for each mac address found.
  netstat  Pulls status from all network devices.
  pull     Pull code in.
  push     Pushes code out.
  reboot   Reboots device.
  remove   Remove Mariachi devices.