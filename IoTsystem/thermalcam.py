from gpiozero
from keyvaluefordict import *
import requests


def thermal_cam_main():
    print("temp")


class thermalcamSend():
    def __init__(self):
        self.API_LOCATION  = "http://localhost:8080/cloudservice/"
        self.STOREID = 1

