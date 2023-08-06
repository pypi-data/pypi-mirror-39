"""
Library containing the implementations of Eumel DataLogger integration classes
"""
import time
from xml.etree import ElementTree

import requests

from core.integration import EnergyDataSource
from core import RawEnergyData, EnergyAsset


class DataLoggerV1(EnergyDataSource):
    """
    Eumel DataLogger api v1.0 access implementation
    """

    def __init__(self, ip, user, password):
        """
        :param ip: Data loggers network IP
        :param user: User configured on the devices
        :param password: Password for this user
        """
        self.eumel_api_url = ip + '/rest'
        self.auth = (user, password)

    def read_state(self, path=None) -> RawEnergyData:
        if path:
            tree = ElementTree.parse('test_examples/EumelXMLOutput.xml')
        else:
            http_packet = requests.get(self.eumel_api_url, auth=self.auth)
            raw = http_packet.content.decode()
            tree = ElementTree.parse(raw)
        tree_root = tree.getroot()
        tree_header = tree_root[0].attrib
        tree_leaves = {child.attrib['id']: child.text for child in tree_root[0][0]}
        device = EnergyAsset(
            manufacturer=tree_header['man'],
            model=tree_header['mod'],
            serial_number=tree_header['sn'])
        access_timestamp = int(time.time())
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        accumulated_power = float(tree_leaves['TotWhImp'].replace('.', ''))
        measurement_timestamp = int(time.mktime(time.strptime(tree_header['t'], time_format)))
        return RawEnergyData(device, access_timestamp, raw, accumulated_power, measurement_timestamp)


class DataLoggerV2d1d1(EnergyDataSource):
    """
    Eumel DataLogger api v2.1.1 access implementation
    """

    def __init__(self, ip, user, password):
        """
        :param ip: Data loggers network IP
        :param user: User configured on the devices
        :param password: Password for this user
        """
        self.eumel_api_url = ip + '/wizard/public/api/rest'
        self.auth = (user, password)

    def read_state(self, path=None) -> RawEnergyData:
        if path:
            tree = ElementTree.parse('test_examples/EumelXMLv2.1.1.xml')
            with open(path) as file:
                raw = file.read()
        else:
            http_packet = requests.get(self.eumel_api_url, auth=self.auth)
            raw = http_packet.content.decode()
            tree = ElementTree.ElementTree(ElementTree.fromstring(raw))
        tree_root = tree.getroot()
        tree_header = tree_root[0].attrib
        tree_leaves = {child.attrib['id']: child.text for child in tree_root[0][1]}
        device = EnergyAsset(
            manufacturer=tree_header['man'],
            model=tree_header['mod'],
            serial_number=tree_header['sn'],
            geolocation=None)
        access_timestamp = int(time.time())
        time_format = '%Y-%m-%dT%H:%M:%SZ'
        accumulated_power = float(tree_leaves['TotWhImp'])
        measurement_timestamp = int(time.mktime(time.strptime(tree_header['t'], time_format)))
        return RawEnergyData(device, access_timestamp, str(raw), accumulated_power, measurement_timestamp)