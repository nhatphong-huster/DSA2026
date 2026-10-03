"""
Mô hình dữ liệu đại diện cho Nhân viên giao hàng (Shipper).
"""

class Shipper:
    def __init__(self, shipper_id: str, name: str, phone: str,
                 current_district: str, max_capacity_kg: float = 30.0):
        self.shipper_id = shipper_id
        self.name = name
        self.phone = phone
        self.current_district = current_district.upper().strip()
        self.max_capacity_kg = float(max_capacity_kg)
        self.assigned_orders = []

    @property
    def current_load_kg(self) -> float:
        return sum(order.weight_kg for order in self.assigned_orders)

    @property
    def remaining_capacity_kg(self) -> float:
        return max(0.0, self.max_capacity_kg - self.current_load_kg)

    def can_carry(self, weight_kg: float) -> bool:
        return self.current_load_kg + weight_kg <= self.max_capacity_kg

    def assign_order(self, order) -> bool:
        if self.can_carry(order.weight_kg):
            self.assigned_orders.append(order)
            order.status = "ASSIGNED"
            return True
        return False

    def clear_deliveries(self):
        self.assigned_orders.clear()

    def __repr__(self):
        return (f"Shipper({self.shipper_id} - {self.name}, "
                f"Tải: {self.current_load_kg:.1f}/{self.max_capacity_kg}kg, "
                f"Vị trí: {self.current_district})")
