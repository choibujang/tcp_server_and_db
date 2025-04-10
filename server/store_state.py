import threading
from models.visitor import Visitor
from models.cart import Cart


class StoreState:
    def __init__(self):
        self.visitors = {}  # {member_id: Visitor}
        self.visitor_lock = threading.Lock()
        self.fruits = {}  # {fruit_id: [fruit_name, price, stock]}
        self.available_carts = set(range(1, 5))
        self.using_carts = set()
        self.cart_lock = threading.Lock()

    def add_visitor(self, member_id, visitor):
        with self.visitor_lock:
            self.visitors[member_id] = visitor

    def is_visitor_in_store(self, member_id):
        with self.visitor_lock:
            return self.visitors.get(member_id)
        
    def remove_visitor(self, member_id):
        with self.visitor_lock:
            if member_id in self.visitors:
                del self.visitors[member_id]

    def allocate_cart(self):
        """사용 가능한 바구니 하나 할당하고 반환 (없으면 None)"""
        with self.cart_lock:
            if not self.available_carts:
                return None
            cart = self.available_carts.pop()
            self.using_carts.add(cart)
            return cart

    def release_cart(self, cart):
        """사용 중인 바구니 반납"""
        with self.cart_lock:
            self.using_carts.discard(cart)
            self.available_carts.add(cart)

    
store_state = StoreState()