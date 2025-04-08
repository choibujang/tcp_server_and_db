from PyQt5.QtCore import QObject, pyqtSignal, QThread, QMetaObject, Qt
from PyQt5.QtNetwork import QTcpServer, QTcpSocket, QAbstractSocket, QHostAddress
import json
from server.client_thread import ClientThread

class TcpServer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.server = QTcpServer()
        self.server.newConnection.connect(self.on_new_connection)
        self.client_threads = []

    def startServer(self, port=1001):
        if self.server.listen(QHostAddress.Any, port):
            print(f"Server started on port {port}")
        else:
            print(f"Server failed to start: {self.server.errorString()}")

    @pyqtSlot()
    def on_new_connection(self):
        while self.server.hasPendingConnections():
            socket = self.server.nextPendingConnection()
            print("Client connected!")
            client_thread = ClientThread(socket)
            self.client_threads.append(client_thread)
            client_thread.start()
        
    def stopServer(self):
        for client_thread in self.client_threads:
            client_thread.stop()
            client_thread.wait()   # 스레드 종료 대기
        self.client_threads.clear()
        super().close()
        print("Server stopped.")


class DataRecvThread(QThread):
    def __init__(self, socket_descriptor, parent=None):
        super().__init__(parent)
        self.socket_descriptor = socket_descriptor
        self.client_socket = None

    def run(self):
        print(f"DataRecvThread started...")
        self.client_socket = QTcpSocket()

        if not self.client_socket.setSocketDescriptor(self.socket_descriptor):
            print(f"Error occured while setSocketDescriptor in Server")
            return # 스레드 실행 종료. finished 시그널 emit -> 스레드 객체 메모리에서 해제
        
        print(f"New client connected: {self.client_socket.peerAddress().toString()}:{self.client_socket.peerPort()}")

        self.client_socket.readyRead.connect(self.readData)
        self.client_socket.disconnected.connect(self.clientDisconnected)
        self.client_socket.errorOccurred.connect(lambda error: self.clientError(error))

        self.exec_()
           

    def readData(self):
        if not self.client_socket or self.client_socket.state() != QTcpSocket.ConnectedState:
            print("Socket is invalid or disconnected.")
            return
        while self.client_socket.bytesAvailable():
            # PySide2.QtCore.QIODevice.readAll():
            #   Reads all remaining data from the device, and returns it as a byte array.
            print("bytes available")
            data = self.client_socket.readAll().data().decode('utf-8')
            print(f"raw data {data} received")
            json_data = json.loads(data)
            print(f"JSON parsed: {json_data}")
            self.dataRecv.emit(json_data)

    def sendData(self, data):
        print(f"DataRecvThread's sendData got data {data}")
        if not self.client_socket or self.client_socket.state() != QTcpSocket.ConnectedState:
            print("Socket is invalid or disconnected.")
            return

        data = json.dumps(data).encode('utf-8')
        result = self.client_socket.write(data)

        if result == -1:
            print("In DataRecvThread's sendData, failed to write data to the socket")


    def stop(self):
        if self.client_socket:
            print(f"close and delete client_socket")
            self.client_socket.blockSignals(True)
            self.client_socket.close()
            self.client_socket.deleteLater() # Schedules this object for deletion.
            self.client_socket = None
        self.quit() # 이벤트 루프 종료, finished 시그널 emit
        print(f"{self.camera_id}'s DataRecvThread stopped.")

    def clientDisconnected(self):
        self.stop()

    def clientError(self, error):
        if error == QAbstractSocket.RemoteHostClosedError:
            print("Error ignored: RemoteHostClosedError already handled")
            return
        #self.client_socket.close()
        if self.client_socket:
            self.stop()