"""
repository:
- 도메인 객체(Visitor, Cart)의 DB 연동을 담당.
- 도메인 객체는 repository를 통해 DB와 통신하며 직접 SQL을 다루지 않는다.

- insert/update/select/delete 등의 연산을 트랜잭션 단위로 관리하며,
  DB 실패 시 rollback을 보장한다.
- repository는 DB, 도메인 객체는 처리 로직에 집중하도록 분리했다.
"""


from server.db.connection import get_connection

def insert_visitor_and_cart(member_id, cart_cam):
    """
    방문자 입장 시 visit_info 테이블과 cart 테이블에 row를 삽입.
    모든 작업은 트랜잭션으로 처리되며, 중간 실패 시 rollback.
    """
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
    """
    cart 테이블의 cart 상태를 결제 요청(1) 으로 변경
    """
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
    """
    방문자가 퇴장할 때 cart 테이블과 visit_info 테이블을 업데이트
    - cart.purchased = 2
    - visit_info.out_dttm = NOW()
    """
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


    
