import numpy as np

def MaxCornerSpeed(TyreFriction, Gravity, Radius, CrawlConstant):
    return np.sqrt(TyreFriction * Gravity * Radius) + CrawlConstant
    
def TimeToAccelarate(InitialSpeed, FinalSpeed, Acceleration):
    return (FinalSpeed - InitialSpeed) / Acceleration

def TotalStraightDegradation(TyreDegradationRate, TrackSegmentLength, K_Straight):
    return TyreDegradationRate * TrackSegmentLength * K_Straight

def TotalBreakingDegradation(TyreDegradationRate, InitialSpeed, FinalSpeed, K_Braking):
    temp1 = (InitialSpeed/100)**2
    temp2 = (FinalSpeed/100)**2
    return (temp1 - temp2) * K_Braking * TyreDegradationRate

def TotalCornerDegradation(K_Corner, Speed, Radius, TyreDegradationRate):
    return K_Corner * (Speed**2 / Radius) * TyreDegradationRate

def TyreFriction(BaseFrictionCoefficient, TotalDegradation, WeatherMultiplier):
    return (BaseFrictionCoefficient - TotalDegradation) * WeatherMultiplier

def FuelUsed(K_Base, K_Drag, IntialSpeed, FinalSpeed, Distance):
    temp1 = ((IntialSpeed + FinalSpeed) / 2)**2
    return (K_Base + (K_Drag * temp1)) * Distance

def RefuelTime(AmountToRefuel, RefuelRate):
    return AmountToRefuel / RefuelRate

#Own Equation: X = (v_final^2 - V_initial^2)/(2*a)
def BrakingDistance(InitialSpeed, FinalSpeed, Deceleration):
    return (FinalSpeed**2 - InitialSpeed**2) / (2 * Deceleration)

#Own Equation: T = (v_final - V_initial)/ a
def BrakingTime(InitialSpeed, FinalSpeed, Deceleration):
    return (FinalSpeed - InitialSpeed) / Deceleration

def PitStopTime(RefuelTime, TyreSwapTime, BasePitStopTime):
    return RefuelTime + TyreSwapTime + BasePitStopTime

def baseScore(TimeReference, TimeActual):
    return 500000 * (TimeReference / TimeActual) **3

def FuelBonus(Fuelused, FuelSoftCapLimit):
    return -500000 * (1 - (Fuelused / FuelSoftCapLimit)) **2 + 500000

def TyreBonus(TyreDegradationSum, NumberOfBlowots):
    return 100000 * TyreDegradationSum -50000 * NumberOfBlowots
 