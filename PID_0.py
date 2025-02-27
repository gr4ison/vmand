import RPi.GPIO as GPIO
import spidev
import time
from simple-pid import PID # type: ignore
GPIO.setmode(GPIO.BCM) #set GPIO mode

RelayPin1 = 5 #1st from left
RelayPin2 = 6 #2nd from left

GPIO.setup(RelayPin1, GPIO.OUT) #setting GPIO pins as outputs
GPIO.setup(RelayPin2, GPIO.OUT)

spi1 = spidev.SpiDev() #create spidev objects
spi2 = spidev.SpiDev()

#Spi0 ce0 = spi.open(0,0) 
#Spi1 ce0 = spi.open(1,0)
spi1.open(0,0)  #open SPI bus for sensors 
spi2.open(1,0)
#define the SPI devices
spi1.max_speed_hz = 1000000
spi1.mode = 0
spi2.max_speed_hz = 1000000
spi2.mode = 0

def ReadTemp(spi): #reading raw data from thermocouple and converting the data to C
	RawData = spi.xfer([0x00, 0x00])
	temp = ((RawData[0] << 8) | RawData[1]) >> 3
	celsius = temp * 0.25
	return celsius

setpoint1 = 22 #inline heater > 500
pid1 = PID(1.0, 0.1, 0.05, setpoint = setpoint1) #(kp, ki, kd, setpoint = target value)
setpoint2 = 20 #external heater > 120
pid2 = PID(1.0, 0.1, 0.05, setpoint = setpoint2) #(kp, ki, kd, setpoint = target value)
#enabling the pid controllers
pid1.output_limits = (0,1)
pid1.proprtional_on_measurement = False
pid1.sample_time = 0.01
pid2.output_limits = (0,1)
pid2.proprtional_on_measurement = False
pid2.sample_time = 0.01

times1 = []
temps1 = []
times2 = []
temps2 = []

StartTime = time.time()

try:
	while True:
		CurrentTemp1 = ReadTemp(spi1)
		CurrentTemp2 = ReadTemp(spi2)
		print("Inline temperature: {:.2f}C".format(CurrentTemp1))
		print("Wrap-around temperature: {:.2f}C".format(CurrentTemp2))
		
		output1 = pid1(CurrentTemp1)
		output2 = pid2(CurrentTemp2) 
		
		if output1 <= 0.5:
			GPIO.output(RelayPin1, GPIO.HIGH)
		else:
			GPIO.output(RelayPin1, GPIO.LOW)
		
		times1.append(time.time() - StartTime)
		temps1.append(CurrentTemp1)
		time.sleep(0.3)
			
		if output2 <= 0.5:
			GPIO.output(RelayPin2, GPIO.HIGH)
		else:
			GPIO.output(RelayPin2, GPIO.LOW)
						
		times2.append(time.time() - StartTime)
		temps2.append(CurrentTemp2)
		time.sleep(0.3)

except KeyboardInterrupt:
	print("All Done!")

finally:
	GPIO.cleanup()
	spi1.close()
	spi2.close()
