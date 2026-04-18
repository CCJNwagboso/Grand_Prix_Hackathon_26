from dataclasses import dataclass

@dataclass
class car :
    max_speed: float
    accel: float
    brake: float
    limp_constant: float
    crawl_constant: float
    fuel_tank_capacity: float
    initial_fuel: float
    fuel_consumption_rate: float
    current_fuel: float


@dataclass
class track :
    id : int
    type : str
    length_m: float
    radius_m: float


@dataclass
class tyres:
    type: str
    life_span: float
    dry_friction_multiplier: float
    cold_friction_multiplier: float
    light_rain_friction_multiplier: float
    heavy_rain_friction_multiplier: float
    dry_degradation: float
    cold_degradation: float
    light_rain_degradation: float
    heavy_rain_degradation: float
    current_tyre_degradation: float


@dataclass
class weather:
    condition: str
    duration_s: float
    acceleration_multiplier: float
    deceleration_multiplier: float
