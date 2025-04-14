from server.models.fruit import Fruit
"""
장바구니 객체.
물품 업데이트 이벤트를 처리한다.
"""
class Cart:
    def __init__(self, cart_id, cart_cam):
        self.cart_id = cart_id
        self.cart_cam = cart_cam
        self.fruits = {}  # {fruit_id: Fruit}
        self.dirty_cart_fruits = []
        self.purchase = 0

    def update(self, new_data):
        self.data = new_data

    def get_purchased(self):
        return self.purchase
    
    def set_purchased(self, flag):
        self.purchase = flag
    
    def get_cart_fruits(self):
        return self.fruits
    