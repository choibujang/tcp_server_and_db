from server.db.repository import (insert_visitor_and_cart, 
                                  update_cart_purchased,
                                  update_visitor_cart_on_exit)
from server.models.cart import Cart

"""
방문자 객체.
입장, 결제요청, 퇴장 이벤트에 따른 객체 상태 변화와 DB 반영을 책임진다.
"""
class Visitor:
    def __init__(self, visit_id, member_id, member_name, cart):
        self.visit_id = visit_id    # visit_info 테이블의 PK
        self.member_id = member_id  # 고객 고유 ID
        self.member_name = member_name
        self.cart = cart    # 장바구니 객체

    @staticmethod
    def enter_store(member_id, cart_cam):
        """
        입장 처리 로직:
        - visit_info, cart 테이블에 데이터 삽입
        - Visitor, Cart 객체 생성
        - 실패 시 rollback 되고 예외 발생
        """
        try:
            visit_id, member_name, cart_id = insert_visitor_and_cart(member_id, cart_cam)
            
            cart = Cart(cart_id=cart_id, cart_cam=cart_cam)
            visitor = Visitor(visit_id, member_id, member_name, cart)

            return visitor
        
        except Exception as e:
            raise

    def update_purchased_state(self):
        """
        - cart 테이블의 purchased를 1로 업데이트
        - visitor.cart.purchased를 1로 업데이트
        - 실패 시 rollback 되고 예외 발생
        """
        try:
            update_cart_purchased(self)
            self.cart.set_purchased(1)
        except Exception as e:
            raise
    

    def exit_store(self):
        """
        - visit_info 테이블의 out_dttm을 현재 시간으로 업데이트
        - cart 테이블의 purchased를 2로 업데이트
        - visitor.cart.purchased를 2로 업데이트
        - 실패 시 rollback 되고 예외 발생
        """
        try:
            update_visitor_cart_on_exit(self)
        except Exception as e:
            raise

    def get_cart_purchased(self):
        return self.cart.is_purchased()
    
    def set_cart_purchased(self, flag):
        self.cart.set_purchased(flag)
    
    def get_cart_fruits(self):
        return self.cart.get_cart_fruits()
    






