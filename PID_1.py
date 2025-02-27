import RPi.GPIO as GPIO
import time
import serial
from simple_pid import PID

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define relay pin
RelayPin1 = 5
GPIO.setup(RelayPin1, GPIO.OUT)  # Set relay pin as output

# Set up USB serial communication (modify port as needed)
usb_port = "/dev/ttyUSB0"  # Change based on your system
baud_rate = 9600

try:
    ser = serial.Serial(usb_port, baud_rate, timeout=1)
    time.sleep(2)  # Allow time for connection to stabilize
except serial.SerialException:
    print("Could not open USB port. Check connections.")
    exit()

def read_temp():
    """ Reads temperature from the USB-connected thermocouple. """
    ser.write(b"READ\n")  # Adjust command based on device protocol
    line = ser.readline().decode("utf-8").strip()
    try:
        return float(line)
    except ValueError:
        return None

# PID setup
setpoint = 22  # Target temperature
pid = PID(1.0, 0.1, 0.05, setpoint=setpoint)
pid.output_limits = (0, 1)
pid.proportional_on_measurement = False
pid.sample_time = 0.01

times = []
temps = []
StartTime = time.time()

try:
    while True:
        CurrentTemp = read_temp()
        if CurrentTemp is not None:
            print("Temperature: {:.2f}C".format(CurrentTemp))

            output = pid(CurrentTemp)
            if output <= 0.5:
                GPIO.output(RelayPin1, GPIO.HIGH)
            else:
                GPIO.output(RelayPin1, GPIO.LOW)

            times.append(time.time() - StartTime)
            temps.append(CurrentTemp)

        time.sleep(0.3)

except KeyboardInterrupt:
    print("All Done!")

finally:
    GPIO.cleanup()
    ser.close()
