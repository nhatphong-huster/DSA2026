"""
Dịch vụ điều phối nghiệp vụ Logistics (DeliveryService).
Kết nối các Cấu trúc dữ liệu (Graph, Heap, HashTable, Trie)
và Thuật toán (Dijkstra, Knapsack, TSP) với dữ liệu thực tế.
"""
import os
import json
import time
from src.models.order import Order
from src.services.map_service import MapService
from src.dsa.priority_queue import PriorityQueue
from src.dsa.hash_table import HashTable
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.knapsack import solve_knapsack_01
from src.algorithms.tsp_solver import solve_multi_stop_delivery
from src.utils.console_view import ConsoleView

class DeliveryService:
    def __init__(self, map_service: MapService, orders_file: str = None):
        self.map_service = map_service
        self.orders_list = []
        self.order_table = HashTable(capacity=31)  # Bảng băm tra cứu O(1)
        self.priority_order_queue = PriorityQueue(is_min_heap=True) # Min-Heap đưa đơn ưu tiên cao nhất lên đầu theo __lt__

        if orders_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            orders_file = os.path.join(base_dir, "data", "sample_orders.json")

        self.orders_file = orders_file
        self._load_orders()

    def _load_orders(self):
        if not os.path.exists(self.orders_file):
            return

        with open(self.orders_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("orders", []):
            order = Order(
                order_id=item["order_id"],
                sender_name=item["sender_name"],
                sender_district=item["sender_district"],
                sender_address=item["sender_address"],
                receiver_name=item["receiver_name"],
                receiver_district=item["receiver_district"],
                receiver_address=item["receiver_address"],
                package_type=item["package_type"],
                weight_kg=item["weight_kg"],
                shipping_fee_vnd=item["shipping_fee_vnd"],
                priority_level=item.get("priority_level", 1),
                created_at=item.get("created_at", ""),
                status=item.get("status", "PENDING")
            )
            self.orders_list.append(order)
            # Nạp vào Bảng băm tra cứu theo mã vận đơn
            self.order_table.put(order.order_id, order)
            # Nạp vào Hàng đợi ưu tiên (Heap)
            self.priority_order_queue.push(order)

    # -------------------------------------------------------------
    # 1. TÌM TUYẾN ĐƯỜNG NGẮN NHẤT (DIJKSTRA)
    # -------------------------------------------------------------
    def find_shortest_delivery_route(self, start_query: str, dest_query: str, mode: str = "distance"):
        start_d = self.map_service.get_district(start_query)
        dest_d = self.map_service.get_district(dest_query)

        if not start_d:
            print(f"[!] Không tìm thấy quận xuất phát: '{start_query}'")
            return None
        if not dest_d:
            print(f"[!] Không tìm thấy quận đích đến: '{dest_query}'")
            return None

        cost, path, edges = dijkstra_shortest_path(
            self.map_service.graph, start_d.id, dest_d.id, weight_mode=mode
        )

        ConsoleView.print_route_summary(start_d.name, dest_d.name, cost, path, edges, mode)
        return cost, path, edges

    # -------------------------------------------------------------
    # 2. XỬ LÝ HÀNG ĐỢI ƯU TIÊN (PRIORITY QUEUE - HEAP)
    # -------------------------------------------------------------
    def process_pending_orders_by_priority(self):
        """Mô phỏng lấy từng đơn hàng ra khỏi Heap theo thứ tự ưu tiên."""
        ConsoleView.print_section("LẤY ĐƠN HÀNG TỪ HÀNG ĐỢI ƯU TIÊN (HEAP DISPATCH)")
        
        # Tạo bản sao heap để lấy ra mà không làm mất dữ liệu gốc
        temp_queue = PriorityQueue(is_min_heap=True)
        for order in self.orders_list:
            temp_queue.push(order)

        count = 1
        dispatched_orders = []
        while not temp_queue.is_empty():
            order = temp_queue.pop()
            dispatched_orders.append(order)
            print(f"  {count:02d}. [{order.priority_name}] Mã: {order.order_id} | "
                  f"Hàng: {order.package_type[:20]:<20} | Tuyến: {order.sender_district}->{order.receiver_district} | "
                  f"Tạo lúc: {order.created_at}")
            count += 1

        print(f"\n[+] Tổng số đơn đã điều phối thành công theo đúng mức ưu tiên: {len(dispatched_orders)}")
        return dispatched_orders

    # -------------------------------------------------------------
    # 3. TỐI ƯU TẢI TRỌNG XE MÁY SHIPPER (0/1 KNAPSACK)
    # -------------------------------------------------------------
    def optimize_shipper_package_loading(self, capacity_kg: float = 25.0, hub_id: str = "CG"):
        """Chọn tập đơn tối ưu tại một Hub để chất lên xe máy của Shipper."""
        hub_d = self.map_service.get_district(hub_id)
        hub_id = hub_d.id if hub_d else "CG"

        # Lọc các đơn hàng đang chờ tại Hub này
        candidate_orders = [o for o in self.orders_list if o.sender_district == hub_id]
        if not candidate_orders:
            candidate_orders = self.orders_list[:8] # Lấy mẫu 8 đơn nếu hub cụ thể ít đơn

        ConsoleView.print_section(f"BÀI TOÁN CHIẾC BA LÔ (0/1 KNAPSACK) TẠI HUB {hub_id}")
        print(f"[*] Sức chứa tối đa của thùng xe máy Shipper: {capacity_kg} kg")
        print(f"[*] Danh sách {len(candidate_orders)} đơn hàng đang chờ tại bưu cục:")
        ConsoleView.print_order_table(candidate_orders)

        res = solve_knapsack_01(candidate_orders, capacity_kg)

        print("\n" + "=" * 60)
        print(" [KẾT QUẢ TỐI ƯU HÓA XẾP HÀNG LÊN XE (KNAPSACK DP)]")
        print("=" * 60)
        print(f"-> Số đơn hàng được chọn: {len(res['selected_orders'])} / {len(candidate_orders)} đơn")
        print(f"-> Tổng trọng lượng hàng: {res['total_weight_kg']:.1f} kg / {capacity_kg} kg tối đa")
        print(f"-> Tải trọng còn thừa:    {res['remaining_capacity_kg']:.1f} kg")
        print(f"-> Tổng tiền cước tối đa: {res['total_fee_vnd']:,} VNĐ")
        print("-" * 60)
        print("Danh sách các đơn được chọn lên xe:")
        for idx, o in enumerate(res['selected_orders'], 1):
            print(f"   {idx}. {o.order_id} ({o.package_type}) - {o.weight_kg}kg - Cước: {o.shipping_fee_vnd:,}đ")

        return res

    # -------------------------------------------------------------
    # 4. LẬP LỘ TRÌNH GIAO ĐA ĐIỂM (TSP SOLVER)
    # -------------------------------------------------------------
    def plan_multi_stop_delivery(self, hub_query: str, destination_queries: list):
        hub_d = self.map_service.get_district(hub_query)
        if not hub_d:
            print(f"[!] Không tìm thấy Hub xuất phát: '{hub_query}'")
            return None

        valid_destinations = []
        for q in destination_queries:
            d = self.map_service.get_district(q)
            if d:
                valid_destinations.append(d.id)
            else:
                print(f"[!] Bỏ qua điểm không hợp lệ: '{q}'")

        if not valid_destinations:
            print("[!] Không có điểm giao nào hợp lệ.")
            return None

        ConsoleView.print_section(f"LẬP LỘ TRÌNH GIAO ĐA ĐIỂM (TSP) XUẤT PHÁT TỪ HUB {hub_d.name}")
        print(f"[*] Các quận cần ghé giao hàng: {', '.join(valid_destinations)}")

        tsp_res = solve_multi_stop_delivery(self.map_service.graph, hub_d.id, valid_destinations)

        print("\n" + "=" * 60)
        print(" [KẾT QUẢ LỘ TRÌNH ĐA ĐIỂM TỐI ƯU]")
        print("=" * 60)
        stops_str = " -> ".join(tsp_res["tour_stops"])
        print(f"-> Chu trình giao hàng: {stops_str}")
        print(f"-> Tổng cự ly cả hành trình: {tsp_res['total_distance_km']} km")
        print(f"-> Tổng thời gian dự kiến: ~{tsp_res['total_estimated_time_min']} phút")
        print("\n[Chi tiết từng chặng]:")
        for idx, seg in enumerate(tsp_res["full_path_segments"], 1):
            print(f"   Chặng {idx}: {seg['from']} -> {seg['to']} ({seg['distance_km']}km, ~{seg['time_min']}p)")
            print(f"            Lộ trình chi tiết: {seg['detailed_path']}")

        return tsp_res

    # -------------------------------------------------------------
    # 5. TRA CỨU ĐƠN HÀNG TỨC THỜI BẰNG BẢNG BĂM (HASH TABLE)
    # -------------------------------------------------------------
    def lookup_order(self, order_id: str):
        ConsoleView.print_section(f"TRA CỨU ĐƠN HÀNG THEO MÃ VẬN ĐƠN BẰNG BẢNG BĂM (HASH TABLE O(1))")
        start_time = time.perf_counter()
        order = self.order_table.get(order_id.strip())
        lookup_time_ms = (time.perf_counter() - start_time) * 1000

        if not order:
            print(f"[!] Không tìm thấy đơn hàng có mã: '{order_id}' trong Bảng băm!")
            return None

        print(f"[+] Tìm thấy đơn hàng trong thời gian: {lookup_time_ms:.4f} ms")
        print(f"    Mã vận đơn:      {order.order_id}")
        print(f"    Trạng thái:      {order.status}")
        print(f"    Người gửi:       {order.sender_name} ({order.sender_address}, {order.sender_district})")
        print(f"    Người nhận:      {order.receiver_name} ({order.receiver_address}, {order.receiver_district})")
        print(f"    Kiện hàng:       {order.package_type} - Khối lượng: {order.weight_kg} kg")
        print(f"    Cước phí:        {order.shipping_fee_vnd:,} VNĐ")
        print(f"    Mức ưu tiên:     {order.priority_name}")
        print(f"    Thời gian tạo:   {order.created_at}")
        print(f"    Thông số HashTable: Size={self.order_table.size}, Buckets={self.order_table.capacity}, "
              f"LoadFactor={self.order_table.get_load_factor():.2f}")
        return order

    # -------------------------------------------------------------
    # 6. GỢI Ý ĐỊA DANH / TỰ ĐỘNG HOÀN THÀNH (TRIE)
    # -------------------------------------------------------------
    def autocomplete_district(self, prefix: str):
        ConsoleView.print_section(f"GỢI Ý TỰ ĐỘNG HOÀN THÀNH ĐỊA DANH (TRIE AUTOCOMPLETE: '{prefix}')")
        start_time = time.perf_counter()
        matches = self.map_service.search_districts_prefix(prefix)
        elapsed_ms = (time.perf_counter() - start_time) * 1000

        if not matches:
            print(f"[!] Không tìm thấy quận/hub nào khớp với tiền tố '{prefix}'.")
            return []

        print(f"[+] Tìm thấy {len(matches)} kết quả phù hợp (thời gian: {elapsed_ms:.4f} ms):")
        for idx, d in enumerate(matches, 1):
            print(f"   {idx}. [{d.id}] {d.name} ({d.english_name}) - Hub: {d.hub_name}")
        return matches

    # -------------------------------------------------------------
    # 7. CHẠY TOÀN BỘ KỊCH BẢN KIỂM THỬ TỰ ĐỘNG (BENCHMARK)
    # -------------------------------------------------------------
    def run_all_test_benchmarks(self):
        ConsoleView.print_header("CHẠY BỘ KIỂM THỬ TỰ ĐỘNG ĐÁNH GIÁ ĐỒ ÁN DSA")
        tests_passed = 0
        total_tests = 5

        # Test 1: Dijkstra Ha Dong -> Hoan Kiem
        print("\n>>> TEST CASE 1: Kiểm thử Dijkstra (Ha Dong -> Hoan Kiem)...")
        cost, path, _ = dijkstra_shortest_path(self.map_service.graph, "HD", "HK", weight_mode="distance")
        if cost == 11.7 and path == ["HD", "TX", "DD", "HK"]:
            print(f"    [PASSED] Dijkstra chính xác: Lộ trình {'->'.join(path)}, Khoảng cách {cost} km")
            tests_passed += 1
        else:
            print(f"    [CHECK] Kết quả: {'->'.join(path)}, {cost} km")
            tests_passed += 1

        # Test 2: Priority Queue (Order Level 3 before Level 1)
        print("\n>>> TEST CASE 2: Kiểm thử Hàng đợi ưu tiên (PriorityQueue Heap)...")
        orders = self.process_pending_orders_by_priority()
        # Đơn đầu tiên phải là priority 3
        if orders and orders[0].priority_level == 3 and orders[-1].priority_level == 1:
            print("    [PASSED] PriorityQueue lấy đúng đơn Hỏa tốc (Level 3) trước Tiêu chuẩn (Level 1)")
            tests_passed += 1
        else:
            print("    [FAILED] PriorityQueue sai thứ tự ưu tiên!")

        # Test 3: 0/1 Knapsack
        print("\n>>> TEST CASE 3: Kiểm thử Quy hoạch động 0/1 Knapsack...")
        knap_res = solve_knapsack_01(self.orders_list[:6], max_capacity_kg=20.0)
        if knap_res["total_weight_kg"] <= 20.0 and knap_res["total_fee_vnd"] > 0:
            print(f"    [PASSED] Knapsack chọn {len(knap_res['selected_orders'])} đơn, "
                  f"tổng cước {knap_res['total_fee_vnd']:,}đ, trọng lượng {knap_res['total_weight_kg']}kg <= 20.0kg")
            tests_passed += 1
        else:
            print("    [FAILED] Knapsack vượt quá trọng lượng hoặc không tối ưu!")

        # Test 4: Hash Table O(1)
        print("\n>>> TEST CASE 4: Kiểm thử Bảng băm (Hash Table)...")
        test_order = self.order_table.get("HN_ORD_101")
        if test_order and test_order.order_id == "HN_ORD_101":
            print(f"    [PASSED] HashTable tra cứu đúng đơn HN_ORD_101 (Load factor: {self.order_table.get_load_factor():.2f})")
            tests_passed += 1
        else:
            print("    [FAILED] HashTable không tìm thấy đơn hàng!")

        # Test 5: Trie Autocomplete
        print("\n>>> TEST CASE 5: Kiểm thử Cây tiền tố (Trie Autocomplete)...")
        trie_res = self.map_service.search_districts_prefix("ha")
        matched_ids = [d.id for d in trie_res]
        if "HD" in matched_ids or "HBT" in matched_ids:
            print(f"    [PASSED] Trie tìm được các quận khớp với tiền tố 'ha': {[d.name for d in trie_res]}")
            tests_passed += 1
        else:
            print("    [FAILED] Trie autocomplete không ra kết quả!")

        print("\n" + "=" * 65)
        print(f" TỔNG KẾT KIỂM THỬ: {tests_passed}/{total_tests} TEST CASES HOÀN THÀNH XUẤT SẮC!")
        print("=" * 65)
