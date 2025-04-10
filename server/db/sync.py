from server.models.cart import Cart
from server.models.visitor import Visitor
from server.store_state import store_state


"""
store_state.visitors를 DB와 연동한다.
"""
def sync_visitors_to_db(cursor):
    """현재 매장에 체류중인 고객의 정보를 가져온다."""
    cursor.execute("""
                   SELECT m.member_name, vi.member_id, vi.visit_id 
                   FROM visit_info vi
                   JOIN members m ON m.member_id = vi.member_id
                   WHERE vi.out_dttm IS NULL;
                   """)
    
    data = cursor.fetchall()
    for row in data:
        member_name, member_id, visit_id = row
        """현재 매장에 체류중인 고객의 카트 정보를 가져온다."""
        cursor.execute("SELECT cart_id, cart_cam, purchased FROM cart WHERE visit_id = %s", (visit_id,))
        cart_data = cursor.fetchone()
        cart_id, cart_cam, purchased = cart_data
        c = Cart(cart_id, cart_cam)
        store_state.using_carts.add(cart_cam)
        store_state.available_carts.difference_update(store_state.using_carts)
        c.purchase = purchased

        """현재 매장에 체류중인 고객의 카트에 담긴 과일 정보를 가져온다."""
        cursor.execute("""
                        SELECT cf.fruit_id, cf.quantity, f.fruit_name, f.price
                        FROM cart_fruit cf 
                        JOIN fruit f ON cf.fruit_id = f.fruit_id
                        WHERE cf.cart_id = %s;
                        """, (cart_id,))
        cart_fruits = cursor.fetchall()
        if not cart_data:
            continue
        else:
            for fruit in cart_fruits:
                fruit_id, quantity, fruit_name, price = fruit
                c.fruits[fruit_id] = [fruit_name, quantity, price]

        v = Visitor(visit_id, member_id, member_name, c)
        store_state.visitors[member_id] = v

"""
store_state.fruits를 DB와 연동한다.
"""
def sync_fruits_to_db(cursor):
    """과일 정보를 DB에서 가져온다."""
    cursor.execute("SELECT fruit_id, fruit_name, price, stock FROM fruit")
    data = cursor.fetchall()
    for row in data:
        fruit_id, fruit_name, price, stock = row
        store_state.fruits[fruit_id] = [fruit_name, price, stock]
