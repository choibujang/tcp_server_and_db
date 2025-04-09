class Fruit:
    def __init__(self, fruit_id, fruit_name, price, stock):
        self.fruit_id = fruit_id
        self.fruit_name = fruit_name
        self.price = price
        self.stock = stock

    def __str__(self):
        return (
            f"Fruit(fruit_id={self.fruit_id}, fruit_name={self.fruit_name}, "
            f"price={self.price}, stock={self.stock})"
        )

    def __repr__(self):
        return self.__str__()