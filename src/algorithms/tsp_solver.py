"""
Giải thuật lập lộ trình giao hàng đa điểm (Travelling Salesperson Problem - TSP).
Áp dụng: Shipper xuất phát từ Hub -> đi giao hàng tại K quận khác nhau -> quay về Hub.
Phương pháp: Heuristic Nearest Neighbor (Láng giềng gần nhất) kết hợp ma trận khoảng cách Dijkstra.
Độ phức tạp: O(K^2 * ((V + E) log V)) với K là số điểm giao hàng.
"""
from src.dsa.graph import Graph
from src.algorithms.dijkstra import dijkstra_shortest_path

def solve_multi_stop_delivery(graph: Graph, start_hub: str, destination_districts: list):
    """
    Tìm lộ trình giao đa điểm cho Shipper khép vòng về Hub.
    
    Tham số:
    - graph: Đồ thị mạng lưới 12 quận Hà Nội.
    - start_hub: Mã quận/Hub xuất phát (VD: 'CG').
    - destination_districts: Danh sách các quận cần giao (VD: ['BD', 'HK', 'DD']).

    Trả về:
    - dict:
        + tour_stops: Danh sách điểm dừng theo thứ tự giao hàng [start, stop1, stop2, ..., start]
        + full_path_segments: Danh sách chi tiết các chặng di chuyển (qua các quận trung gian)
        + total_distance_km: Tổng cự ly cả hành trình
        + total_estimated_time_min: Tổng thời gian dự kiến (phút)
    """
    start_hub = start_hub.upper().strip()
    # Loại bỏ điểm trùng lặp và loại bỏ chính start_hub khỏi danh sách cần ghé nếu có
    destinations = list(set(d.upper().strip() for d in destination_districts if d.upper().strip() != start_hub))

    if not destinations:
        return {
            "tour_stops": [start_hub, start_hub],
            "full_path_segments": [],
            "total_distance_km": 0.0,
            "total_estimated_time_min": 0
        }

    unvisited = set(destinations)
    current_node = start_hub
    tour_stops = [start_hub]
    full_path_segments = []
    total_distance = 0.0
    total_time = 0

    # Bước lặp Tham lam: Luôn chọn điểm chưa ghé thăm có khoảng cách ngắn nhất từ vị trí hiện tại
    while unvisited:
        nearest_next = None
        min_cost = float('inf')
        best_segment_path = []
        best_edges = []

        for candidate in unvisited:
            cost, path, edges = dijkstra_shortest_path(graph, current_node, candidate, weight_mode="distance")
            if cost < min_cost:
                min_cost = cost
                nearest_next = candidate
                best_segment_path = path
                best_edges = edges

        # Di chuyển tới điểm gần nhất
        segment_time = sum(e.base_time_min for e in best_edges)
        full_path_segments.append({
            "from": current_node,
            "to": nearest_next,
            "distance_km": min_cost,
            "time_min": segment_time,
            "detailed_path": " -> ".join(best_segment_path)
        })

        total_distance += min_cost
        total_time += segment_time
        current_node = nearest_next
        tour_stops.append(current_node)
        unvisited.remove(nearest_next)

    # Chặng cuối: Từ điểm dừng cuối cùng quay trở về Hub ban đầu
    return_cost, return_path, return_edges = dijkstra_shortest_path(graph, current_node, start_hub, weight_mode="distance")
    return_time = sum(e.base_time_min for e in return_edges)

    full_path_segments.append({
        "from": current_node,
        "to": start_hub,
        "distance_km": return_cost,
        "time_min": return_time,
        "detailed_path": " -> ".join(return_path)
    })

    total_distance += return_cost
    total_time += return_time
    tour_stops.append(start_hub)

    return {
        "tour_stops": tour_stops,
        "full_path_segments": full_path_segments,
        "total_distance_km": round(total_distance, 2),
        "total_estimated_time_min": total_time
    }
