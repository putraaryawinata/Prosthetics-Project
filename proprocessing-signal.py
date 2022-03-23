import numpy as np
import re

def value_sensor_dataset(sensor_lines_value):
  """
    Parameter:
      sensor_lines_value: ndarray of lines in output result
    Return:
      results: ndarray of sensor value (and timestamp if it exists)
  """
  string = np.array(sensor_lines_value)
  #sample:
  #string = np.array(["A0 23 A1 35 A2 9 A3 14 A4 0 A5 27","A0 26 A1 37 A2 10 A3 13 A4 0 A5 25","A0 16 A1 29 A2 6 A3 8 A4 0 A5 19"])
  results = np.zeros((len(string), 5))
  for i in range(len(string)):
    #If timestamp does not exist
    result = re.search(r"^[A][0][ ](\d*)[ ][A][1][ ](\d*)[ ][A][2][ ](\d*)[ ][A][3][ ](\d*)[ ][A][4][ ](\d*)[ ][A][5][ ](\d*)$", string[0])
    
    #If timestamp exist, use the code below instead
    #result = re.search(r"(.*)[ ][A][0][ ](\d*)[ ][A][1][ ](\d*)[ ][A][2][ ](\d*)[ ][A][3][ ](\d*)[ ][A][4][ ](\d*)[ ][A][5][ ](\d*)$", string[0])
    for j in range(5):
      results[i, j] = int(result.group(j+1))
  return results

sensor = np.array(["A0 23 A1 35 A2 9 A3 14 A4 0 A5 27","A0 26 A1 37 A2 10 A3 13 A4 0 A5 25","A0 16 A1 29 A2 6 A3 8 A4 0 A5 19"])
print(value_sensor_dataset(sensor))
