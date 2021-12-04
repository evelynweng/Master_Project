import threading
import pir
import thermalcam
# call subprocess
t_pirIn = threading.Thread(target= pir.pir_in_main,
                            args=())
t_pirOut = threading.Thread(target= pir.pir_out_main, args=())
t_thermalCam = threading.Thread(target= thermalcam.thermal_cam_main, 
                            args=())

print("starting IoT device")
# exec subprocess
t_pirIn.start()
t_pirOut.start()
t_thermalCam.start()

# wait thread process to end
t_pirIn.join()
t_pirOut.join()
t_thermalCam.join()

print("Exit Service.")