from PyQt5.QtCore import QObject
from PyQt5.QtNetwork import QTcpServer, QHostAddress
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