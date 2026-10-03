"""
Mô hình dữ liệu đại diện cho một Quận nội thành và Hub bưu cục.
"""

class District:
    def __init__(self, id: str, code: str, name: str, english_name: str,
                 hub_name: str, hub_address: str, latitude: float, longitude: float,
                 traffic_density_factor: float = 1.0):
        self.id = id.upper()                           # VD: "CG", "HK", "BD"
        self.code = code                               # VD: "cau_giay"
        self.name = name                               # VD: "Cầu Giấy"
        self.english_name = english_name               # VD: "Cau Giay"
        self.hub_name = hub_name                       # Tên bưu cục trung chuyển
        self.hub_address = hub_address                 # Địa chỉ bưu cục
        self.latitude = latitude                       # Vĩ độ
        self.longitude = longitude                     # Kinh độ
        self.traffic_density_factor = traffic_density_factor # Hệ số mật độ giao thông

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "english_name": self.english_name,
            "hub_name": self.hub_name,
            "hub_address": self.hub_address,
            "traffic_density_factor": self.traffic_density_factor
        }

    def __repr__(self):
        return f"District({self.id} - {self.name}, Hub: {self.hub_name})"
