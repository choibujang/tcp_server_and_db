import asyncio
import websockets
from multiprocessing import Queue

async def handle_client(websocket, path, queue):
    camera_id = int(await websocket.recv())  # 첫 메시지로 카메라 ID 받음
    print(f"Camera {camera_id} connected")

    try:
        while True:
            frame_binary = await websocket.recv()  # 바이너리 데이터 수신
            queue.put((camera_id, frame_binary))  # PyQt로 전달

    except websockets.ConnectionClosed:
        print(f"Camera {camera_id} disconnected")

async def start_server(queue):
    print("WebSocket server started on ws://localhost:8765")
    async with websockets.serve(lambda ws, path: handle_client(ws, path, queue), "localhost", 8765):
        await asyncio.Future()  # 서버 유지

def run_websocket_server(queue):
    asyncio.run(start_server(queue))
