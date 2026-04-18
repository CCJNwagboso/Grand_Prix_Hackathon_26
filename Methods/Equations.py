import numpy as np

def MaxCornerSpeed(TyreFriction, Gravity, Radius, CrawlConstant):
    return np.sqrt(TyreFriction * Gravity * Radius) + CrawlConstant
    
