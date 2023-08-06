"""
Library containing the implementations of smart-meter simulator integration classes
"""
import random
import time

from core.integration import EnergyDataSource
from core import RawEnergyData, EnergyAsset


class EnergyMeter(EnergyDataSource):
    """
    Data logger simulator. It will return a pseudo-random incremental number in every iteration
    """

    def __init__(self):
        self.memory = random.randint(1, 20)

    def read_state(self) -> RawEnergyData:
        access_timestamp = int(time.time())
        device = EnergyAsset(
            manufacturer='Slock.it',
            model='Virtual Energy Meter',
            serial_number='0001000',
            geolocation=(1.123, 1.321))
        accumulated_power = random.randint(self.memory, (self.memory + 1) + 20)
        measurement_timestamp = int(time.time())
        device_str = device.manufacturer + device.model + device.serial_number
        raw = str(device_str + str(access_timestamp) + str(accumulated_power) + str(measurement_timestamp))
        return RawEnergyData(device, access_timestamp, raw, accumulated_power, measurement_timestamp)
