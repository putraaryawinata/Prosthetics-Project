import serial
import re
import time
import bionic_model as bm

if __name__ == '__main__':
    # SET SERIAL VALUE OF ARDUINO ON RASPI
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.flush()

    while True:
        if ser.in_waiting > 0:
            # READLINE FROM ARDUINO
            try:
                line = ser.readline().decode('utf-8').rstrip()
                data = re.search(r"A0 (.*) A1 (.*) A2 (.*) A3 (.*) A4 (.*) A5 (.*)", line)
            except:
                print('masalah dengan readline')
            try:
                sensor_value = [data.group(1), data.group(2), data.group(3), data.group(4), data.group(5), data.group(6)]
            except:
                continue
            # CONVERT SENSOR VALUE TO SUDUT
            sudut = bm.convert_sensor_into_sudut('bionicleg_model2.tflite', sensor_value)
            print(sudut)

            # PASS SUDUT BACK TO ARDIONO
            str_i = str(sudut) + '\n'
            ser.write(str.encode(str_i))
            #time.sleep(0.001)
