import numpy as np
from numpy import loadtxt

MIN_TEMP = 35

def detect_temperature(thermstr):
    data_array = thermstr.split(",")
    results = data_array[(data_array>MIN_TEMP)]
    tempavg = np.mean(results)
    print("temp avg: ", tempavg)
    if tempavg > 38:
        return False
    else: 
        return True
    return False