from pydantic import BaseModel

from greenhouse_lib.models import ActuatorAsset


class ApiPotAsset(BaseModel):
    id: int
    plant: int
    moisture_sensor: int
    moisture: float
    pump: int
    health_sensor: int


class ApiPumpAsset (ActuatorAsset):
    pot: int


class ApiShelfAsset(BaseModel):
    temp_humid_sensor: int
    pots: list[int]
