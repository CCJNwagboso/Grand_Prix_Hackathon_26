from dataclasses import dataclass
from typing import Optional, List


@dataclass
class car:
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
class track:
    id: int
    type: str
    length_m: float
    radius_m: Optional[float] = None


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

    def friction_multiplier(self, condition: str) -> float:
        return {
            "dry":        self.dry_friction_multiplier,
            "cold":       self.cold_friction_multiplier,
            "light_rain": self.light_rain_friction_multiplier,
            "heavy_rain": self.heavy_rain_friction_multiplier,
        }.get(condition, self.dry_friction_multiplier)

    def degradation_rate(self, condition: str) -> float:
        return {
            "dry":        self.dry_degradation,
            "cold":       self.cold_degradation,
            "light_rain": self.light_rain_degradation,
            "heavy_rain": self.heavy_rain_degradation,
        }.get(condition, self.dry_degradation)


@dataclass
class weather:
    condition: str
    duration_s: float
    acceleration_multiplier: float
    deceleration_multiplier: float


@dataclass
class race:
    name: str
    laps: int
    base_pit_stop_time_s: float
    pit_tyre_swap_time_s: float
    pit_refuel_rate: float
    corner_crash_penalty_s: float
    pit_exit_speed: float
    fuel_soft_cap_limit: float
    starting_weather_condition_id: int
    time_reference_s: float


@dataclass
class tyre_set:
    set_id: int
    compound: str
    tyres: tyres


@dataclass
class race_config:
    car: car
    race: race
    track_segments: List[track]
    tyre_sets: List[tyre_set]
    weather_schedule: List[weather]
    starting_tyre_set_id: int = 1