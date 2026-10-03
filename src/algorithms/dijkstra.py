"""
Thuật toán Dijkstra tìm đường đi ngắn nhất / nhanh nhất trên đồ thị có trọng số.
Sử dụng cấu trúc Hàng đợi ưu tiên (PriorityQueue - MinHeap) tự cài đặt.
Độ phức tạp: O((V + E) * log V)
"""
from src.dsa.graph import Graph
from src.dsa.priority_queue import PriorityQueue

def dijkstra_shortest_path(graph: Graph, start_vertex: str, end_vertex: str, weight_mode: str = "distance"):
    """
    Tìm đường đi tối ưu giữa 2 đỉnh trong đồ thị các quận Hà Nội.
    
    Tham số:
    - graph: Đối tượng Graph mạng lưới giao thông.
    - start_vertex: Mã quận xuất phát (VD: 'CG', 'HD').
    - end_vertex: Mã quận đích đến (VD: 'HK', 'BD').
    - weight_mode: 
        + 'distance': Tối ưu khoảng cách ngắn nhất (km)
        + 'time_base': Tối ưu thời gian giờ bình thường (phút)
        + 'time_peak': Tối ưu thời gian giờ cao điểm tránh tắc đường (phút)

    Trả về:
    - (cost, path, edge_details)
    """
    start = start_vertex.upper().strip()
    end = end_vertex.upper().strip()

    all_vertices = graph.get_all_vertices()
    if start not in all_vertices or end not in all_vertices:
        raise ValueError(f"Đỉnh xuất phát '{start}' hoặc đích '{end}' không tồn tại trong đồ thị!")

    # distances lưu chi phí tối ưu từ start đến mỗi đỉnh
    distances = {v: float('inf') for v in all_vertices}
    previous_nodes = {v: None for v in all_vertices}
    previous_edges = {v: None for v in all_vertices}

    distances[start] = 0.0

    # Min-Heap lưu các phần tử: (chi_phí, tên_đỉnh)
    pq = PriorityQueue(is_min_heap=True)
    pq.push((0.0, start))

    visited = set()

    while not pq.is_empty():
        current_cost, current_node = pq.pop()

        if current_node in visited:
            continue
        visited.add(current_node)

        # Đã tới đích thì có thể dừng sớm
        if current_node == end:
            break

        for edge in graph.get_neighbors(current_node):
            neighbor = edge.neighbor

            # Xác định trọng số theo chế độ tối ưu
            if weight_mode == "distance":
                edge_cost = edge.distance_km
            elif weight_mode == "time_peak":
                edge_cost = float(edge.peak_time_min)
            else: # time_base
                edge_cost = float(edge.base_time_min)

            new_cost = current_cost + edge_cost

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous_nodes[neighbor] = current_node
                previous_edges[neighbor] = edge
                pq.push((new_cost, neighbor))

    # Tái tạo đường đi từ end ngược về start
    path = []
    edges_traversed = []
    curr = end

    if distances[end] == float('inf'):
        return float('inf'), [], []

    while curr is not None:
        path.append(curr)
        if previous_edges[curr] is not None:
            edges_traversed.append(previous_edges[curr])
        curr = previous_nodes[curr]

    path.reverse()
    edges_traversed.reverse()

    return round(distances[end], 2), path, edges_traversed
