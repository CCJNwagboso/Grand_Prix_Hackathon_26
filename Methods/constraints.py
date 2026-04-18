from DataClasses.dataClasses import car, track, tyres, weather
import numpy as np
from Methods.Equations import MaxCornerSpeed, TimeToAccelarate, TotalStraightDegradation, TotalBreakingDegradation, TotalCornerDegradation, TyreFriction, FuelUsed, RefuelTime, BrakingDistance, BrakingTime, PitStopTime, baseScore, FuelBonus, TyreBonus

#Check if the current speed is below the crawl speed
#Probably check after decelerating
def MinimumSpeedConstraint(CurrentSpeed, CrawlSpeed):
    if CurrentSpeed < CrawlSpeed:
        return CrawlSpeed
    else:
        return CurrentSpeed

#Only Accelerate in Straights
#Thus if CurrentSpeed > target speed, Continue at CurrentSpeed, else Accelerate to target speed
def SpeedFollowThrough(CurrrentSpeed, TargetSpeed, Acceleration):
    if CurrrentSpeed > TargetSpeed:
        return CurrrentSpeed
    else:
        return TargetSpeed #Do acceleration

#if fuel level is 0 or tyre life span is 0, then speed is limited to limp mode max speed, else continue at current speed
#Also doesn't allow acceleration / deceleration
def LimpMode(CurrentFuelLevel, TyreLifeSpan, LimpModeMaxSpeed, CurrentSpeed):
    if CurrentFuelLevel ==0 or TyreLifeSpan ==0:
        return LimpModeMaxSpeed
    else:
        return CurrentSpeed
    
#When car crashes travel at crawl speed 
#Stuck in this speed till can accelerate at start of straight
def CrawlMode(CrashStatus, CrawlSpeed):
    if CrashStatus == True:
        return CrawlSpeed
    else:
        return None #Continue with normal speed
