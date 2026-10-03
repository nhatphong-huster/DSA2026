"""
Mô hình dữ liệu đại diện cho một Đơn hàng giao vận (Order).
"""

class Order:
    PRIORITY_NAMES = {
        1: "Tiêu chuẩn (Standard)",
        2: "Giao nhanh (Fast)",
        3: "Hỏa tốc (Express)"
    }

    def __init__(self, order_id: str, sender_name: str, sender_district: str, sender_address: str,
                 receiver_name: str, receiver_district: str, receiver_address: str,
                 package_type: str, weight_kg: float, shipping_fee_vnd: int,
                 priority_level: int = 1, created_at: str = "", status: str = "PENDING"):
        self.order_id = order_id.strip()
        self.sender_name = sender_name
        self.sender_district = sender_district.upper().strip()
        self.sender_address = sender_address
        self.receiver_name = receiver_name
        self.receiver_district = receiver_district.upper().strip()
        self.receiver_address = receiver_address
        self.package_type = package_type
        self.weight_kg = float(weight_kg)
        self.shipping_fee_vnd = int(shipping_fee_vnd)
        self.priority_level = int(priority_level)  # 1: Tiêu chuẩn, 2: Nhanh, 3: Hỏa tốc
        self.created_at = created_at
        self.status = status  # PENDING, ASSIGNED, IN_TRANSIT, DELIVERED

    @property
    def priority_name(self) -> str:
        return self.PRIORITY_NAMES.get(self.priority_level, "Không xác định")

    def __lt__(self, other):
        """
        Dùng cho so sánh trong Priority Queue (Heap):
        - Ưu tiên mức độ cao hơn trước (priority_level lớn hơn xếp trước).
        - Nếu cùng mức ưu tiên, đơn nào tạo sớm hơn (created_at nhỏ hơn) xử lý trước (FIFO).
        """
        if self.priority_level != other.priority_level:
            return self.priority_level > other.priority_level
        return self.created_at < other.created_at

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "sender": f"{self.sender_name} ({self.sender_district})",
            "receiver": f"{self.receiver_name} ({self.receiver_district})",
            "package_type": self.package_type,
            "weight_kg": self.weight_kg,
            "shipping_fee_vnd": self.shipping_fee_vnd,
            "priority": self.priority_name,
            "created_at": self.created_at,
            "status": self.status
        }

    def __repr__(self):
        return (f"Order({self.order_id}, {self.sender_district}->{self.receiver_district}, "
                f"{self.weight_kg}kg, {self.shipping_fee_vnd:,}đ, L{self.priority_level})")
