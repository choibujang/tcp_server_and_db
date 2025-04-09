from server.models.cart import Cart
from server.models.visitor import Visitor


"""
DB에 따라 현재 매장 내에 있는 visitor들을 초기화한다.
"""
def sync_db_to_visitor(cursor, visitors, using_carts, available_carts):
    cursor.execute("""
        SELECT  m.member_name, vi.member_id, vi.visit_id, c.cart_id, c.purchased, c.cart_cam, cf.fruit_id, cf.quantity, f.fruit_name, f.price
        FROM 
            members m
        LEFT JOIN 
            visit_info vi ON m.member_id = vi.member_id
        LEFT JOIN 
            cart c ON vi.visit_id = c.visit_id
        LEFT JOIN 
            cart_fruit cf ON c.cart_id = cf.cart_id
        LEFT JOIN 
            fruit f ON cf.fruit_id = f.fruit_id
        WHERE 
            vi.out_dttm IS NULL;
    """)

    data = cursor.fetchall()
    for row in data:
        member_name, member_id, visit_id, cart_id, purchase, cart_cam, fruit_id, quantity, fruit_name, price = row
        if visit_id not in visitors:
            if cart_id and cart_cam:
                c = Cart(cart_id, cart_cam)
                c.purchase = purchase
                using_carts.add(cart_cam)
            else:
                Cart(None, None)
            v = Visitor(visit_id, member_id, member_name, c)
            visitors[visit_id] = v
        if fruit_id:
            visitors[visit_id].cart.data[fruit_id] = [fruit_name, quantity, price]

    available_carts -= using_carts


