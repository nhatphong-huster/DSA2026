"""
Cài đặt Cấu trúc dữ liệu Đồ thị có trọng số (Weighted Graph) bằng Danh sách kề (Adjacency List).
"""

class Edge:
    """Đại diện cho một cạnh nối giữa 2 đỉnh/quận trong đồ thị giao thông."""
    def __init__(self, neighbor: str, distance_km: float, base_time_min: int,
                 peak_time_min: int, route_name: str = ""):
        self.neighbor = neighbor.upper()
        self.distance_km = float(distance_km)
        self.base_time_min = int(base_time_min)
        self.peak_time_min = int(peak_time_min)
        self.route_name = route_name

    def __repr__(self):
        return f"Edge(-> {self.neighbor}, {self.distance_km}km, {self.base_time_min}p, '{self.route_name}')"


class Graph:
    """
    Đồ thị biểu diễn mạng lưới logistics nội thành Hà Nội.
    - Cấu trúc lưu trữ: Danh sách kề (Adjacency List)
    - Không gian lưu trữ: O(V + E) với V là số quận, E là số tuyến đường.
    """
    def __init__(self):
        # adj_list map: vertex_id -> list of Edge objects
        self.adj_list = {}
        # metadata lưu thông tin thêm của đỉnh nếu có
        self.vertex_data = {}

    def add_vertex(self, vertex_id: str, data: dict = None):
        """
        Thêm một đỉnh (quận) vào đồ thị.
        Độ phức tạp: O(1)
        """
        v = vertex_id.upper().strip()
        if v not in self.adj_list:
            self.adj_list[v] = []
            self.vertex_data[v] = data or {}

    def add_edge(self, u: str, v: str, distance_km: float,
                 base_time_min: int = 15, peak_time_min: int = 30,
                 route_name: str = "", bidirectional: bool = True):
        """
        Thêm cạnh nối giữa 2 đỉnh u và v.
        Độ phức tạp: O(1)
        """
        u = u.upper().strip()
        v = v.upper().strip()

        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        edge_uv = Edge(v, distance_km, base_time_min, peak_time_min, route_name)
        self.adj_list[u].append(edge_uv)

        if bidirectional:
            edge_vu = Edge(u, distance_km, base_time_min, peak_time_min, route_name)
            self.adj_list[v].append(edge_vu)

    def get_neighbors(self, vertex_id: str):
        """
        Lấy danh sách các cạnh kề với đỉnh vertex_id.
        Độ phức tạp: O(1)
        """
        v = vertex_id.upper().strip()
        return self.adj_list.get(v, [])

    def get_edge_details(self, u: str, v: str):
        """
        Lấy chi tiết cạnh nối trực tiếp giữa u và v (nếu có).
        Độ phức tạp: O(deg(u))
        """
        u = u.upper().strip()
        v = v.upper().strip()
        for edge in self.get_neighbors(u):
            if edge.neighbor == v:
                return edge
        return None

    def get_all_vertices(self):
        """Trả về toàn bộ danh sách mã đỉnh trong đồ thị."""
        return list(self.adj_list.keys())

    @property
    def num_vertices(self) -> int:
        return len(self.adj_list)

    @property
    def num_edges(self) -> int:
        count = sum(len(edges) for edges in self.adj_list.values())
        return count // 2  # Đồ thị vô hướng

    def __repr__(self):
        return f"Graph(Vertices: {self.num_vertices}, Edges: {self.num_edges})"
