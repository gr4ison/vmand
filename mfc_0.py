import asyncio
from alicat import FlowController

async def get():
    async with FlowController('/dev/ttyUSB0') as flow_controller:
        print(await flow_controller.get())

asyncio.run(get())

flow_controller_1 = FlowController(address='A')
flow_controller_2 = FlowController(address='B')

await flow_controller_1.close() # /dev/ttyUSB0 is still open!
await flow_controller_2.close()
