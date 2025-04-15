"""
FruitcamHandler:
- Fruit camera로부터의 요청을 처리하는 핸들러.
- 과일 재고 업데이트 이벤트를 감지하고 도메인 객체 및 시스템 상태를 제어한다.

- store_state는 리소스(장바구니, 방문자)를 관리한다.
- 이 핸들러는 흐름만 조율한다.
"""

from store_state import store_state
from models.visitor import Visitor

class FruitcamHandler:
    def __init__(self, socket):
        self.socket = socket