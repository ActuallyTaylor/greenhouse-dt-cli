import sys
from dataclasses import dataclass

import dotenv
from influxdb_client.client.influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from urllib3.exceptions import NewConnectionError

class DBConnectionError(Exception):
    pass

@dataclass
class PlantSnapshot:
    shelf: int
    pot: int
    stress: float
    temperature: float
    humidity: float
    nitrogen: float
    moisture: float
    light: float
    ph_level: float

class InfluxDBInterface:

    def __init__(self):

        env_vals = dotenv.dotenv_values()
        token = env_vals["INFLUXDB_TOKEN"]
        if token is None:
            print("Missing INFLUXDB_TOKEN in .env")
            sys.exit()
        self.org = env_vals["INFLUXDB_ORG"] or 'greenhouse'
        self.bucket = env_vals["INFLUXDB_ORG"] or 'greenhouse'
        url = "http://localhost:8086"

        self.client = InfluxDBClient(url, token=token)

    def write_snapshot(self, snapshot: PlantSnapshot):

        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        points = []
        points.append(
            Point("stress")
            .tag("shelf", snapshot.shelf)
            .tag("pot", snapshot.pot)
            .field("stress", snapshot.stress)
        )
        points.append(
            Point("nitrogen")
            .tag("shelf", snapshot.shelf)
            .tag("pot", snapshot.pot)
            .field("nitrogen", snapshot.nitrogen)
        )
        points.append(
            Point("moisture")
            .tag("shelf", snapshot.shelf)
            .tag("pot", snapshot.pot)
            .field("moisture", snapshot.moisture)
        )
        points.append(
            Point("ph_level")
            .tag("shelf", snapshot.shelf)
            .tag("pot", snapshot.pot)
            .field("ph_level", snapshot.ph_level)
        )

        try:
            write_api.write(bucket=self.bucket, org=self.org, record=points)
        except NewConnectionError:
            raise DBConnectionError
