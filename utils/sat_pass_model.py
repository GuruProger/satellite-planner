from dataclasses import dataclass
from datetime import datetime


@dataclass
class SatellitePassModel:
	name: str
	rise: datetime
	fall: datetime
	elevation: float


@dataclass
class SatelliteParamModel:
	latitude: float
	longitude: float
	altitude: float
	horizon: float
	minimum_culmination: float
	start_time: datetime
	flight_length: int
