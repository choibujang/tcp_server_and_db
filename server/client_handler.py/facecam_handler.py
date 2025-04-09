from store_state import store_state
from db.connection import *
from models.cart import Cart
from models.visitor import Visitor

class FacecamHandler:
    def __init__(self, socket):
        self.socket = socket

    def handle(self, payload):
        data = payload.get("data", [])  # [ {"member_id": 1 , “action”: “visit“} ]
        member_id = data[0].get("member_id")
        action = data[0].get("action")

        visitor = store_state.is_visitor_in_store(member_id)

        """
        방문한 손님의 경우 DB에 방문 정보를 저장하고 카트를 할당한다.
        """
        if not visitor:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO visit_info (member_id, in_dttm) VALUES (%s, NOW())",
                (member_id,)
            )
            cursor.execute("SELECT LAST_INSERT_ID()")
            visit_id = cursor.fetchone()[0]
            conn.commit()

            cursor.execute("select member_name from members where member_id=%s", (member_id,))
            member_name = cursor.fetchone()[0]

            cart_cam = store_state.allocate_cart()

            cursor.execute("insert into cart (visit_id, cart_cam, purchased) values (%s, %s, %s)", (visit_id, cart_cam, 0))
            cart_id = cursor.execute("SELECT LAST_INSERT_ID()")
            conn.commit()

            c = Cart(cart_id=cart_id, cart_cam=cart_cam)
            v = Visitor(visit_id, member_id, member_name, c)

            store_state.visitors.add_visitor(member_id, v)
            
            cursor.close()
            conn.close()
        else:
            """
            고객이 쇼핑을 마치고 계산하려는 경우 카트에 담긴 물품의 이름, 개수, 가격을 반환해준다.
            """
            res = []
            if visitor.cart.purchase == 0:
                for fruit in visitor.cart.fruits:
                    res.append({"Item": fruit.fruit_name, "Count": fruit.stock, "Price": fruit.price})
            
            self.socket.write(res)

            visitor.cart.purchase = 1

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("update cart set purchased=1 where cart_id=%s", (visitor.cart.cart_id,))
            conn.commit()
            cursor.close()
            conn.close()

            """
            고객이 장바구니에 담은 물품 정보를 확인하고 결제하려는 경우, 결제 정보를 DB에 업데이트하고 고객 객체를 삭제한다.
            """
            if visitor.cart.purchase == 1:
                if action == "yes":
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("update cart set purchased=%s, pur_dttm=NOW() where cart_id=%s", (2, visitor.cart.cart_id))
                    cursor.execute("update visit_info set out_dttm=NOW() where visit_id=%s", (visitor.visit_id,))
                    conn.commit()
                    conn.close()
                    cursor.close()

                    store_state.remove_visitor(visitor.member_id)


                




