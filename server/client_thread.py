from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtNetwork import QTcpSocket
import json

class ClientThread(QThread):
    def __init__(self, socket: QTcpSocket):
        super().__init__()
        self.socket = socket
        self.socket.moveToThread(self)  # 메인 스레드에서 만들어진 socket을 현재 QThread로 옮김김

    def run(self):
        self.socket.readyRead.connect(self.on_ready_read)
        self.socket.disconnected.connect(self.on_disconnected)
        self.exec_()

    def on_ready_read(self):
        try:
            data = self.socket.readAll().data().decode()
            payload = json.loads(data)
            camera_id = payload.get("camera_id")

            if camera_id == "entry":
                self.handle_entry(payload)
            elif camera_id == "basket":
                self.handle_basket(payload)
            elif camera_id == "checkout":
                self.handle_checkout(payload)
            else:
                self.socket.write(b"Unknown camera_id\n")
        except Exception as e:
            print("에러:", e)
            self.socket.write(b"Invalid data\n")

    def on_disconnected(self):
        print("disconnected from client")
        self.socket.close()
        self.socket.deleteLater()
        self.quit()
        self.wait()