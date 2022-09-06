import configparser
import os
from datetime import datetime


config_name = "config.ini"


class Config:
    """The config in this example only holds devices."""

    def __init__(self):
        self.path = os.getcwd()
        self.devices = {}

    def add_device(self, mac):
        s_mac = str(mac)
        print(self.devices)
        ts = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if s_mac in self.devices:
            self.devices[s_mac]["last_seen"] = ts
        else:
            self.devices[s_mac] = {
                "last_seen": ts
            }

    def read_config(self):
        parser = configparser.RawConfigParser()
        parser.read([config_name])
        try:
            self.devices.update(parser.items("devices"))
        except configparser.NoSectionError:
            pass

    def write_config(self):
        parser = configparser.RawConfigParser()
        parser.add_section("devices")
        for key, value in self.devices.items():
            parser.set("devices", key, value)
        with open(config_name, "w") as file:
            parser.write(file)
