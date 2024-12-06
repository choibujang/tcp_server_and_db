import threading
import queue
import json
import time
from custom_classes import *

visitors = {}
carts = {}
cart_cam_available = queue.Queue()

class DataProcessorThread(threading.Thread):
    def __init__(self, camera_id, data_queue):
        super().__init__()
        self.camera_id = camera_id
        self.data_queue = data_queue  # 카메라 스레드에서 전달받는 데이터를 처리
        self._is_running = True

    def run(self):
        """카메라 데이터 처리"""
        while self._is_running:
            try:
                # 큐에서 데이터 가져오기
                data = self.data_queue.get(timeout=1)  # 1초 대기 후 큐 비어 있으면 예외 발생
                parsed_data = json.loads(data)

                print(f"데이터 처리 스레드 (카메라 {self.camera_id}): 데이터 처리 -> {parsed_data}")
                self.data_queue.task_done()  # 처리 완료
            except queue.Empty:
                pass  # 큐가 비어 있으면 대기
            except Exception as e:
                print(f"데이터 처리 스레드 (카메라 {self.camera_id}): 처리 중 오류 발생 -> {str(e)}")

    def stop(self):
        """스레드 중지"""
        self._is_running = False

    def process_cart_cam(parsed_data):
        data = parsed_data


    def process_face_cam(self, parsed_data):
        data = parsed_data
        member_id = data["member_id"]
        # create visit_info row, cart row in db and get visit_id, cart_id
        cart_id = None
        visit_id = None

        visitor = Visitor(visit_id, member_id, time.time())
        visitors[visit_id] = visitor

        cart = Cart(cart_id, visit_id)
        carts[cart_id] = cart
        self.thread_manager.add_camera() 





