class Visitor:
    def __init__(self, visit_id, member_id, member_name, cart):
        self.visit_id = visit_id
        self.member_id = member_id
        self.member_name = member_name
        self.cart = cart

    def __str__(self):
        return (
            f"Visitor(visit_id={self.visit_id}, member_id={self.member_id}, "
            f"cart={self.cart})"
        )

    def __repr__(self):
        return self.__str__()