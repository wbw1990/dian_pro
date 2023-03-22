import asyncio
import websockets

async def hello():
    try:
        async with websockets.connect('ws://127.0.0.1:8765/light/on') as websocket:
            light_addr = '00-12-4b-01'
            await websocket.send(light_addr)
            recv_msg = await websocket.recv()
            print("client:" + recv_msg)
    except websockets.exceptions.ConnectionClosedError as e:
        print("connection closed error")
    except Exception as e:
        print(e)

# if __name__ == "__main__":
hello()