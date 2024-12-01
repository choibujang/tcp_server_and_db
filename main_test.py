from multiprocessing import Process, Queue
from websocket_server_test import run_websocket_server
from qt_app_test import run_pyqt_app

if __name__ == "__main__":
    # 프로세스 간 통신을 위한 큐 생성
    queue = Queue()

    # WebSocket 서버 프로세스 실행
    websocket_process = Process(target=run_websocket_server, args=(queue,))
    websocket_process.start()

    # PyQt 애플리케이션 실행
    run_pyqt_app(queue)

    # WebSocket 서버 프로세스 종료
    websocket_process.join()
