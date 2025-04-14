from server.db.connection import get_connection

def insert_visitor_and_cart(member_id, cart_cam):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO visit_info (member_id, in_dttm) VALUES (%s, NOW())",
            (member_id,)
        )
        cursor.execute("SELECT LAST_INSERT_ID()")
        visit_id = cursor.fetchone()[0]

        cursor.execute("select member_name from members where member_id=%s", (member_id,))
        member_name = cursor.fetchone()[0]

        cursor.execute("insert into cart (visit_id, cart_cam, purchased) values (%s, %s, %s)", (visit_id, cart_cam, 0))
        cursor.execute("SELECT LAST_INSERT_ID()")
        cart_id = cursor.fetchone()[0]

        conn.commit()

        return visit_id, member_name, cart_id
        
    except Exception as e:
        conn.rollback()
        print(f"Error occured while inserting new visitor into database:{e}")
        raise
    finally:
        cursor.close()
        conn.close()

def update_cart_purchased(visitor):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("update cart set purchased=1 where cart_id=%s", 
                    (visitor.cart.cart_id,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error occured while updating cart table's purchased:{e}")
        raise
    finally:
        cursor.close()
        conn.close()

def update_visitor_cart_on_exit(visitor):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("update cart set purchased=%s, pur_dttm=NOW() where cart_id=%s", 
                    (2, visitor.cart.cart_id))
        cursor.execute("update visit_info set out_dttm=NOW() where visit_id=%s", 
                    (visitor.visit_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error occured while updating visit_info, cart's exit: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


    
