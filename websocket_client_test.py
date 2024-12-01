import asyncio
import websockets
import cv2
import base64
import time

async def send_video(camera_id):
    uri = "ws://localhost:8765"  # PyQt WebSocket 서버 주소
    async with websockets.connect(uri) as websocket:
        # 카메라 ID를 서버에 전송
        await websocket.send(str(camera_id))

        cap = cv2.VideoCapture(camera_id)  # 카메라 ID에 따라 비디오 캡처
        if not cap.isOpened():
            print(f"Camera {camera_id} could not be opened.")
            return

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"Camera {camera_id} failed to capture frame.")
                    break

                # 프레임을 JPEG로 인코딩
                _, buffer = cv2.imencode('.jpg', frame)

                # WebSocket으로 전송
                await websocket.send(buffer.tobytes())
                await asyncio.sleep(0.03)  # 약 30 FPS
        finally:
            cap.release()

if __name__ == "__main__":
    # 카메라 클라이언트 실행 (예: Camera 0, 1, 2)
    import sys
    camera_id = int(sys.argv[1])  # 카메라 ID를 명령줄 인수로 전달
    asyncio.run(send_video(camera_id))
