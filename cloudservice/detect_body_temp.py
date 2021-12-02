import numpy as np
import base64

MIN_TEMP = 32
MAX_TEMP = 34
mlx_shape = (24,32)

def detect_temperature(temps_string):
    vector_bytes_str_enc = base64.b64decode(temps_string)
    temp_array = np.frombuffer(vector_bytes_str_enc)
    data_array = (np.reshape(temp_array,mlx_shape)) # reshape to 24x32
    results = data_array[(data_array>MIN_TEMP)]
    u = np.mean(results)
    
    if u > MAX_TEMP:
        return False
    return True