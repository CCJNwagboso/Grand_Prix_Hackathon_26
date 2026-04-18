import numpy as np
from DataClasses.dataClasses import car, track, tyres, weather
from Methods.equations import *

def brake(InitialSpeed, FinalSpeed, Deceleration, TyreDegradationRate, K_Braking, TrackSegmentLength, K_Straight, K_Base, tyre: tyres, weather: weather, car: car, K_Drag=0):
    brake_dist = BrakingDistance(InitialSpeed, FinalSpeed, Deceleration)
    brake_time = BrakingTime(InitialSpeed, FinalSpeed, Deceleration)
    straight_degradation = TotalStraightDegradation(TyreDegradationRate, brake_dist, K_Straight)
    braking_degradation = TotalBreakingDegradation(TyreDegradationRate, InitialSpeed, FinalSpeed, K_Braking)
    fuel_used = FuelUsed(K_Base, K_Drag, InitialSpeed, FinalSpeed, brake_dist)
    current_fuel = car.current_fuel - fuel_used
    total_degradation = straight_degradation + braking_degradation
    tyre_friction = TyreFriction(tyre.BaseFrictionCoefficient, total_degradation, weather.WeatherMultiplier)
    return brake_dist, brake_time, total_degradation, current_fuel, tyre_friction


def accelerate(InitialSpeed, FinalSpeed, Acceleration, TyreDegradationRate, K_Straight, K_Base, tyre: tyres, weather: weather, car: car, K_Drag=0):
    accel_time = TimeToAccelarate(InitialSpeed, FinalSpeed, Acceleration)
    accel_dist = (InitialSpeed * accel_time) + (0.5 * Acceleration * accel_time**2)
    straight_degradation = TotalStraightDegradation(TyreDegradationRate, accel_dist, K_Straight)
    fuel_used = FuelUsed(K_Base, K_Drag, InitialSpeed, FinalSpeed, accel_dist)
    current_fuel = car.current_fuel - fuel_used
    tyre_friction = TyreFriction(tyre.BaseFrictionCoefficient, straight_degradation, weather.WeatherMultiplier)
    return accel_dist, accel_time, straight_degradation, current_fuel, tyre_friction

def corner(Speed, Radius, TyreDegradationRate, K_Corner, K_Base, tyre: tyres, weather: weather, track: track, car: car, K_Drag=0):
    corner_degradation = TotalCornerDegradation(K_Corner, Speed, Radius, TyreDegradationRate)
    tyre_friction = TyreFriction(tyre.BaseFrictionCoefficient, corner_degradation, weather.WeatherMultiplier)
    fuel_used = FuelUsed(K_Base, K_Drag, Speed, Speed, track.length_m)
    current_fuel = car.current_fuel - fuel_used
    corner_time = track.length_m / Speed
    return corner_degradation, tyre_friction, current_fuel, corner_time


def straight(Speed, TrackSegmentLength, TyreDegradationRate, K_Straight, K_Base, tyre: tyres, weather: weather, car: car, K_Drag=0):
    straight_degradation = TotalStraightDegradation(TyreDegradationRate, TrackSegmentLength, K_Straight)
    tyre_friction = TyreFriction(tyre.BaseFrictionCoefficient, straight_degradation, weather.WeatherMultiplier)
    fuel_used = FuelUsed(K_Base, K_Drag, Speed, Speed, TrackSegmentLength)
    current_fuel = car.current_fuel - fuel_used
    straight_time = TrackSegmentLength / Speed
    return straight_degradation, tyre_friction, current_fuel, straight_time


class pit_stop:
    def __init__(self, RefuelTime, TyreSwapTime, BasePitStopTime):
        self.RefuelTime = RefuelTime
        self.TyreSwapTime = TyreSwapTime
        self.BasePitStopTime = BasePitStopTime


    def refuel(self, AmountToRefuel, RefuelRate, car: car):
        refuel_time = RefuelTime(AmountToRefuel, RefuelRate)
        current_fuel = car.current_fuel + AmountToRefuel
        if current_fuel > car.fuel_tank_capacity:
            current_fuel = car.fuel_tank_capacity
        self.RefuelTime = refuel_time
        return refuel_time, current_fuel
    
    def tyre_swap(self, TyreSwapTime, car: car, tyre: tyres):
        self.TyreSwapTime = TyreSwapTime
        current_tyre_degradation = 0
        return TyreSwapTime, current_tyre_degradation


    def total_pit_stop_time(self):
        return PitStopTime(self.RefuelTime, self.TyreSwapTime, self.BasePitStopTime)




