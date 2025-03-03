import asyncio
from alicat import FlowController
import serial

#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust baud rate if needed
#ser.write(b'flow?\r')  # Example command for Alicat
#response = ser.readline()
#print(response.decode('utf-8'))
#ser.close()

async def get():
    async with FlowController('/dev/ttyUSB0') as flow_controller:
        print(await flow_controller.get())

asyncio.run(get())

flow_controller_1 = FlowController(address='A')
flow_controller_2 = FlowController(address='B')
