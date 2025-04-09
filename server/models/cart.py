class Cart:
    def __init__(self, cart_id, cart_cam):
        self.cart_id = cart_id
        self.cart_cam = cart_cam
        self.fruits = []
        self.purchase = 0

    def update(self, new_data):
        self.data = new_data

    def get_data(self):
        return self.data.copy()
    
    def __str__(self):
        return (
            f"Cart(cart_id={self.cart_id}, cart_cam={self.cart_cam}, "
            f"data={self.data}), "
            f"purchase={self.purchase}"
        )

    def __repr__(self):
        return self.__str__()