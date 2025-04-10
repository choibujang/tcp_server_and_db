from db.connection import get_connection
from db.sync import sync_visitors_to_db, sync_fruits_to_db

from server.store_state import store_state
from server.tcp_server import TcpServer


if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()

    sync_visitors_to_db(cursor)
    print("visitors initialized")

    sync_fruits_to_db(cursor)
    print("fruits initialized")

    cursor.close()
    conn.close()

    tcp_server = TcpServer()
    tcp_server.startServer(port=1001)





