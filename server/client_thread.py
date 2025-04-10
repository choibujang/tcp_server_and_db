from PyQt5.QtCore import QThread
from PyQt5.QtNetwork import QTcpSocket
import json
from server.client_handler.facecam_handler import FacecamHandler

class ClientThread(QThread):
    def __init__(self, socket: QTcpSocket):
        super().__init__()
        self.socket = socket
        self.socket.moveToThread(self)  # 메인 스레드에서 만들어진 socket을 현재 QThread로 옮김
        self.camera_id = None
        self.handler = None

    def run(self):
        self.socket.readyRead.connect(self.on_ready_read)
        self.socket.disconnected.connect(self.on_disconnected)
        self.exec_()

    def on_ready_read(self):
        try:
            data = self.socket.readAll().data().decode()
            payload = json.loads(data)

            if self.handler == None:
                camera_id = payload.get("camera_id")
                self.handler = self.create_handler(camera_id)

                if self.handler is None:
                    self.socket.write(b"Unknown camera_id\n")
                    self.socket.disconnectFromHost()
 
            self.handler.handle(payload)
        except Exception as e:
            print("에러:", e)
            self.socket.write(b"Invalid data\n")

    def create_handler(self, camera_id):
        if camera_id == "Face":
            return FacecamHandler(self.socket)
        elif camera_id == "Fruit":
            return FruitcamHandler(self.socket)
        elif camera_id == "Cart":
            return CartcamHandler(self.socket)
        return None

    def on_disconnected(self):
        print("disconnected from client")
        self.socket.close()
        self.socket.deleteLater()
        self.quit()
        self.wait()