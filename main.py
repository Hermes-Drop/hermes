import os
import asyncio
import websockets

# main code file
# abstracted camera and servo control handled here
# send and receive socket code handled here

# send camera feed to user-control
async def send(websocket):
	await websocket.send("Hermes Connected to User Control...")

# receive control data from user-control
async def receive(websocket):
	try:
		while True:
			test_msg = await websocket.recv()
			if test_msg:
				await websocket.send("Hermes Connected to User Control... (Receive Function)")
				# await send("Hermes Connected to User Control (Send from Receive Function)")
				print(f"Received: {test_msg}")
	except Exception as e:
		print(f"Error: {e}")
	finally:
		await websocket.close()
# initialize the websocket server for the client to connect to
async def main():
	async with websockets.serve(receive, "localhost", 8765):
		print("Hermes Initialized...")
		await asyncio.Future()

asyncio.run(main())
