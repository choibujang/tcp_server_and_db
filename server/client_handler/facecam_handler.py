"""
FacecamHandler:
- Face camera로부터의 요청을 처리하는 핸들러.
- 방문, 결제 요청, 퇴장 이벤트를 감지하고 도메인 객체 및 시스템 상태를 제어한다.

- 이벤트 처리 로직은 Visitor 객체가 책임진다.
- store_state는 리소스(장바구니, 방문자)를 관리한다.
- 이 핸들러는 흐름만 조율한다.
"""

from store_state import store_state
from models.visitor import Visitor

class FacecamHandler:
    def __init__(self, socket):
        self.socket = socket

    def handle(self, payload):
        data = payload.get("data", [])  # [ {"member_id": 1 , “action”: “visit“} ]
        member_id = data[0].get("member_id")
        action = data[0].get("action")

        visitor = store_state.is_visitor_in_store(member_id)

        if not visitor:    
            """
            방문 이벤트:
            - 고객은 반드시 카트를 가지므로 먼저 cart_cam을 할당
            - Visitor 객체와 새로운 DB row를 생성한다
            - 생성 실패 시, 카트는 반환하고 에러 응답
            """
            cart_cam = store_state.allocate_cart()
            try:
                visitor = Visitor.enter_store(member_id, cart_cam)
                store_state.add_visitor(member_id, visitor)
            except Exception as e:
                store_state.release_cart_cam(cart_cam)
                print(f"failed to enter: {e}: release cart")
                self.socket.write({"error": "failed to enter"})

        else:
            res = []
            try:
                """
                결제 요청 이벤트:
                - 장바구니에 담긴 물품을 확인시켜준다.
                - 구매 확인을 기다리는 상태로 상태 업데이트 (purchased = 1)
                """
                if visitor.get_purchased() == 0:

                    for fruit_id, fruit in visitor.get_cart_fruits():
                        res.append({"Item": fruit.name, "Count": fruit.stock, "Price": fruit.price})
                    
                    visitor.update_purchased_state()

                elif visitor.get_purchased() == 1:
                    """
                    구매 확인 이벤트:
                    - action == "yes" → 결제 확정 및 퇴장 처리
                    - action == "no" → 결제 요청 전 상태로 변경 (purchased = 0)
                    """
                    if action == "yes":
                        visitor.exit_store()

                        store_state.release_cart_cam(visitor.cart_cam)
                        store_state.remove_visitor(visitor.member_id)
                    else:
                        visitor.set_purchased(0)
                        res.append({"Item": "cancel"})
            
            except Exception as e:
                print(f"Error occured: {e}")
                res.clear()
                res.append({"Item": "error"})
            finally:
                self.socket.write(res)
            


                




