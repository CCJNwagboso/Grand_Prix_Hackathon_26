import numpy as np
from DataClasses.dataClasses import car, track, tyres, weather
from Methods.equations import (
    BrakingDistance, BrakingTime, TimeToAccelarate,
    TotalStraightDegradation, TotalBreakingDegradation, TotalCornerDegradation,
    TyreFriction, FuelUsed, RefuelTime, PitStopTime,
)


def brake(InitialSpeed, FinalSpeed, Deceleration, K_Braking, K_Straight, K_Base,
          tyre: tyres, weather: weather, car: car, K_Drag=0):
    brake_dist           = BrakingDistance(InitialSpeed, FinalSpeed, Deceleration)
    brake_time           = BrakingTime(InitialSpeed, FinalSpeed, Deceleration)
    straight_degradation = TotalStraightDegradation(tyre.degradation_rate(weather.condition), brake_dist, K_Straight)
    braking_degradation  = TotalBreakingDegradation(tyre.degradation_rate(weather.condition), InitialSpeed, FinalSpeed, K_Braking)
    total_degradation    = straight_degradation + braking_degradation
    fuel_used            = FuelUsed(K_Base, K_Drag, InitialSpeed, FinalSpeed, brake_dist)
    current_fuel         = car.current_fuel - fuel_used
    tyre_friction        = TyreFriction(tyre.friction_multiplier(weather.condition), total_degradation, 1.0)
    return brake_dist, brake_time, total_degradation, current_fuel, tyre_friction


def accelerate(InitialSpeed, FinalSpeed, Acceleration, K_Straight, K_Base,
               tyre: tyres, weather: weather, car: car, K_Drag=0):
    accel_time           = TimeToAccelarate(InitialSpeed, FinalSpeed, Acceleration)
    accel_dist           = (InitialSpeed * accel_time) + (0.5 * Acceleration * accel_time**2)
    straight_degradation = TotalStraightDegradation(tyre.degradation_rate(weather.condition), accel_dist, K_Straight)
    fuel_used            = FuelUsed(K_Base, K_Drag, InitialSpeed, FinalSpeed, accel_dist)
    current_fuel         = car.current_fuel - fuel_used
    tyre_friction        = TyreFriction(tyre.friction_multiplier(weather.condition), straight_degradation, 1.0)
    return accel_dist, accel_time, straight_degradation, current_fuel, tyre_friction


def corner(Speed, Radius, K_Corner, K_Base, tyre: tyres, weather: weather, segment: track, car: car, K_Drag=0):
    corner_degradation = TotalCornerDegradation(K_Corner, Speed, Radius, tyre.degradation_rate(weather.condition))
    tyre_friction      = TyreFriction(tyre.friction_multiplier(weather.condition), corner_degradation, 1.0)
    fuel_used          = FuelUsed(K_Base, K_Drag, Speed, Speed, segment.length_m)
    current_fuel       = car.current_fuel - fuel_used
    corner_time        = segment.length_m / Speed
    return corner_degradation, tyre_friction, current_fuel, corner_time


def straight(Speed, K_Straight, K_Base, tyre: tyres, weather: weather, segment: track, car: car, K_Drag=0):
    straight_degradation = TotalStraightDegradation(tyre.degradation_rate(weather.condition), segment.length_m, K_Straight)
    tyre_friction        = TyreFriction(tyre.friction_multiplier(weather.condition), straight_degradation, 1.0)
    fuel_used            = FuelUsed(K_Base, K_Drag, Speed, Speed, segment.length_m)
    current_fuel         = car.current_fuel - fuel_used
    straight_time        = segment.length_m / Speed
    return straight_degradation, tyre_friction, current_fuel, straight_time


class pit_stop:
    def __init__(self, BasePitStopTime: float):
        self.BasePitStopTime = BasePitStopTime
        self._refuel_time    = 0.0
        self._tyre_swap_time = 0.0

    def refuel(self, AmountToRefuel: float, RefuelRate: float, car: car):
        self._refuel_time = RefuelTime(AmountToRefuel, RefuelRate)
        current_fuel = min(car.current_fuel + AmountToRefuel, car.fuel_tank_capacity)
        return self._refuel_time, current_fuel

    def tyre_swap(self, TyreSwapTime: float):
        self._tyre_swap_time = TyreSwapTime
        return TyreSwapTime, 0.0

    def total_pit_stop_time(self):
        return PitStopTime(self._refuel_time, self._tyre_swap_time, self.BasePitStopTime)