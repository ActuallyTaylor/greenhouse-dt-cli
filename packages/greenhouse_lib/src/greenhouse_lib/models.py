from enum import Enum

from pydantic import BaseModel


class PlantHealthState(int, Enum):
    HEALTHY = 0
    UNHEALTHY = 1
    DEAD = 2


class PlantAsset(BaseModel):
    id: int
    family: str
    ndvi: float
    health_state: PlantHealthState


class PotAsset(BaseModel):
    id: int
    plant: PlantAsset
    moisture_sensor: MoistureSensorAsset
    moisture: float
    pump: PumpAsset
    health_sensor: HealthSensorAsset


class SensorAsset(BaseModel): 
    id: int
    sensor_value: float


class MoistureSensorAsset(SensorAsset):
    pass


class LightSensorAsset(SensorAsset):
    pass

class TempHumiditySensorAsset(SensorAsset):
    temperature_value: float
    humidity_value: float

class PHSensorAsset(SensorAsset):
    pass

class NitrogenSensorAsset(SensorAsset):
    pass

class HealthSensorAsset(SensorAsset):
    pass

class NutrientSensorAsset(SensorAsset):
    pass

class ActuatorAsset(BaseModel):
    id: int
    power_state: bool

class LightSwitchAsset (ActuatorAsset):
    pass

class PumpAsset (ActuatorAsset):
    pot: PotAsset

class ShelfAsset(BaseModel):
    temp_humid_sensor: TempHumiditySensorAsset
    pots: list[PotAsset]


class GreenhouseAsset(BaseModel):
    light_sensor: LightSensorAsset
    light_switch: LightSwitchAsset
    shelves: list[ShelfAsset]
    