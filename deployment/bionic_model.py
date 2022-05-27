import numpy as np
from tflite_runtime.interpreter import Interpreter

# DEFINE FUNCTION TO CONVERT SENSOR INTO SUDUT
def convert_sensor_into_sudut(model_path='bionicleg_model.tflite', input=[0, 0, 0, 0, 0, 0]):
    # GET MODEL TENSORFLOW
    interpreter = Interpreter(model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # GET SENSORS VALUE
    sensor_value = np.array(input, dtype=np.int64) # perlu diganti sesuai inputnya

    # CONVERT NOW FROM SENSOR TO SUDUT
    interpreter.set_tensor(input_details[0]['index'], sensor_value.reshape(1, 6))
    interpreter.invoke()
    sudut = interpreter.get_tensor(output_details[0]['index'])

    return sudut[0, 0]
