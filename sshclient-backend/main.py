import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send('222')

async def start_server():
    server = await websockets.serve(echo, 'localhost', 7070)
    await server.wait_closed()

asyncio.get_event_loop().run_until_complete(start_server())
