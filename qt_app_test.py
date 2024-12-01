import sys
import cv2
import numpy as np
import base64
from multiprocessing import Queue
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer, Qt


class VideoStreamApp(QWidget):
    def __init__(self, queue):
        super().__init__()
        self.setWindowTitle("Multi-Camera Video Stream")
        self.setGeometry(100, 100, 1200, 800)

        # QLabel 생성 (카메라 3대)
        self.camera_labels = [QLabel(f"Camera {i}") for i in range(3)]
        for label in self.camera_labels:
            label.setAlignment(Qt.AlignCenter)
            label.setFixedSize(400, 300)

        # 레이아웃 설정
        layout = QVBoxLayout()
        for label in self.camera_labels:
            layout.addWidget(label)
        self.setLayout(layout)

        # 큐와 타이머 설정
        self.queue = queue
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        while not self.queue.empty():
            camera_id, frame_binary = self.queue.get()  # 바이너리 데이터 수신
            frame = self.decode_frame(frame_binary)  # 바이너리 데이터 디코딩
            self.update_label(camera_id, frame)  # QLabel 업데이트
            

    def decode_frame(self, frame_binary):
        # OpenCV로 바이너리 데이터 디코딩
        frame = np.frombuffer(frame_binary, np.uint8)
        return cv2.imdecode(frame, cv2.IMREAD_COLOR)


    def update_label(self, camera_id, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = width * channel
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.camera_labels[camera_id].setPixmap(pixmap)


def run_pyqt_app(queue):
    app = QApplication(sys.argv)
    viewer = VideoStreamApp(queue)
    viewer.show()
    sys.exit(app.exec_())
