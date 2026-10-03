"""
Dịch vụ quản lý Bản đồ giao thông 12 quận nội thành Hà Nội.
Nạp dữ liệu từ JSON, khởi tạo Đồ thị (Graph) và Cây tiền tố (Trie).
"""
import os
import json
from src.models.district import District
from src.dsa.graph import Graph
from src.dsa.trie import Trie

class MapService:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Lấy đường dẫn thư mục data tương đối từ file này
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            data_dir = os.path.join(base_dir, "data")

        self.data_dir = data_dir
        self.districts = {}       # map: district_id -> District object
        self.graph = Graph()
        self.trie = Trie()

        self._load_districts()
        self._load_graph()

    def _load_districts(self):
        districts_file = os.path.join(self.data_dir, "hanoi_districts.json")
        if not os.path.exists(districts_file):
            raise FileNotFoundError(f"Không tìm thấy file: {districts_file}")

        with open(districts_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("districts", []):
            d = District(
                id=item["id"],
                code=item["code"],
                name=item["name"],
                english_name=item["english_name"],
                hub_name=item["hub_name"],
                hub_address=item["hub_address"],
                latitude=item["latitude"],
                longitude=item["longitude"],
                traffic_density_factor=item.get("traffic_density_factor", 1.0)
            )
            self.districts[d.id] = d
            self.graph.add_vertex(d.id, d.to_dict())

            # Nạp vào cây Trie: nạp cả ID, tên tiếng Việt và tên không dấu để tra cứu
            self.trie.insert(d.id, d)
            self.trie.insert(d.name, d)
            self.trie.insert(d.english_name, d)

    def _load_graph(self):
        graph_file = os.path.join(self.data_dir, "hanoi_graph.json")
        if not os.path.exists(graph_file):
            raise FileNotFoundError(f"Không tìm thấy file: {graph_file}")

        with open(graph_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for edge in data.get("edges", []):
            self.graph.add_edge(
                u=edge["from"],
                v=edge["to"],
                distance_km=edge["distance_km"],
                base_time_min=edge.get("base_time_min", 15),
                peak_time_min=edge.get("peak_time_min", 30),
                route_name=edge.get("route_name", ""),
                bidirectional=edge.get("bidirectional", True)
            )

    def get_district(self, query: str) -> District:
        """Tìm quận theo ID hoặc tên."""
        q = query.upper().strip()
        if q in self.districts:
            return self.districts[q]

        for d in self.districts.values():
            if d.name.lower() == query.strip().lower() or d.english_name.lower() == query.strip().lower():
                return d
        return None

    def search_districts_prefix(self, prefix: str) -> list:
        """Dùng Trie để tìm kiếm gợi ý địa danh."""
        matches = self.trie.autocomplete(prefix)
        # Loại bỏ các kết quả District trùng lặp
        unique_districts = {}
        for word, district_obj in matches:
            if district_obj and district_obj.id not in unique_districts:
                unique_districts[district_obj.id] = district_obj
        return list(unique_districts.values())

    def get_all_districts(self) -> list:
        return list(self.districts.values())
