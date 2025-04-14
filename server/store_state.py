import threading
from models.visitor import Visitor
from models.cart import Cart


class StoreState:
    def __init__(self):
        self.visitors = {}  # {member_id: Visitor}
        self.visitor_lock = threading.Lock()
        self.fruits = {}  # {fruit_id: [fruit_name, price, stock]}
        self.available_cart_cams = set(range(1, 5))
        self.using_cart_cams = set()
        self.cart_cam_lock = threading.Lock()

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

    def allocate_cart_cam(self):
        """사용 가능한 바구니 하나 할당하고 반환 (없으면 None)"""
        with self.cart_cam_lock:
            if not self.available_cart_cams:
                return None
            cart_cam = self.available_cart_cams.pop()
            self.using_cart_cams.add(cart_cam)
            return cart_cam

    def release_cart_cam(self, cart_cam):
        """사용 중인 바구니 반납"""
        with self.cart_cam_lock:
            self.using_cart_cams.discard(cart_cam)
            self.available_cart_cams.add(cart_cam)

    
store_state = StoreState()