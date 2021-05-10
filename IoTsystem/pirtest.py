from gpiozero import MotionSensor

PIR_IN = MotionSensor(4) # motion sensor on GPIO 4 for IN
while True:
    PIR_IN.wait_for_motion ()
    print("detected")
    # send http post request to server to update count
