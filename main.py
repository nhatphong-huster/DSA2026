"""
=============================================================================
   HỆ THỐNG GIAO HÀNG THÔNG MINH NỘI THÀNH HÀ NỘI (HANOI LOGISTICS)
         Đồ Án: Cấu Trúc Dữ Liệu & Giải Thuật (DSA) - Năm 2026
=============================================================================
File chạy chính toàn bộ hệ thống (Main Entry Point).
Tích hợp:
  - Graph (Adjacency List) & Dijkstra (Shortest Path Routing)
  - Priority Queue (Binary Heap) cho phân luồng đơn hàng
  - Dynamic Programming (0/1 Knapsack) cho tối ưu tải trọng xe máy Shipper
  - TSP Solver (Nearest Neighbor Heuristic) cho giao hàng đa điểm
  - Hash Table (Separate Chaining) cho tra cứu mã vận đơn O(1)
  - Trie (Prefix Tree) cho tìm kiếm và tự động gợi ý địa danh
"""

import sys
from src.services.map_service import MapService
from src.services.delivery_service import DeliveryService
from src.utils.console_view import ConsoleView

def print_banner():
    ConsoleView.print_header("HỆ THỐNG GIAO HÀNG NỘI THÀNH HÀ NỘI (H-LOGISTICS)", width=72)

def print_menu():
    print("\n" + "=" * 72)
    print("                      [MENU CHỨC NĂNG HỆ THỐNG]")
    print("=" * 72)
    print("  1. [Graph & Dijkstra]      Tìm tuyến đường giao hàng ngắn nhất giữa 2 quận")
    print("  2. [Priority Queue / Heap] Điều phối đơn hàng theo mức ưu tiên (Hỏa tốc)")
    print("  3. [0/1 Knapsack DP]       Tối ưu hóa tải trọng hàng lên xe máy của Shipper")
    print("  4. [TSP Solver]            Lập lộ trình giao hàng đa điểm cho Shipper")
    print("  5. [Hash Table O(1)]       Tra cứu chi tiết đơn hàng theo Mã vận đơn")
    print("  6. [Trie Autocomplete]     Tìm kiếm và gợi ý tên quận / Hub bưu cục")
    print("  7. [Danh sách dữ liệu]     Xem danh sách 12 quận & đơn hàng hiện có")
    print("  8. [Kiểm thử tự động]      Chạy kịch bản đánh giá toàn diện hệ thống")
    print("  0. Thoát chương trình")
    print("-" * 72)

def handle_show_data(map_service: MapService, delivery_service: DeliveryService):
    print("\n--- A. DANH SÁCH 12 QUẬN NỘI THÀNH VÀ HUB TRUNG CHUYỂN ---")
    districts = map_service.get_all_districts()
    print(f"{'MÃ':<5} | {'TÊN QUẬN':<15} | {'HUB TRUNG CHUYỂN':<32} | {'MẬT ĐỘ GT':<10}")
    print("-" * 70)
    for d in districts:
        print(f"{d.id:<5} | {d.name:<15} | {d.hub_name:<32} | {d.traffic_density_factor:<10.1f}")

    print("\n--- B. DANH SÁCH ĐƠN HÀNG ĐANG CÓ TRONG HỆ THỐNG ---")
    ConsoleView.print_order_table(delivery_service.orders_list)

def main():
    print("\n[+] Đang nạp dữ liệu bản đồ Hà Nội và danh sách đơn hàng...")
    try:
        map_service = MapService()
        delivery_service = DeliveryService(map_service)
        print(f"[OK] Đã nạp thành công {map_service.graph.num_vertices} quận, "
              f"{map_service.graph.num_edges} tuyến đường và {len(delivery_service.orders_list)} đơn hàng mẫu.")
    except Exception as e:
        print(f"[!] Lỗi khi nạp dữ liệu: {e}")
        sys.exit(1)

    print_banner()

    while True:
        print_menu()
        choice = input("Nhập lựa chọn của bạn (0-8): ").strip()

        if choice == "1":
            ConsoleView.print_section("1. TÌM ĐƯỜNG ĐI TỐI ƯU (DIJKSTRA)")
            print("Gợi ý: 'Ha Dong', 'Hoan Kiem', 'Cau Giay', 'Ba Dinh', 'Dong Da', 'Long Bien'...")
            start = input("-> Nhập quận gửi (hoặc mã quận): ").strip()
            dest = input("-> Nhập quận nhận (hoặc mã quận): ").strip()
            print("   Chế độ tối ưu:")
            print("     1. Theo Khoảng cách ngắn nhất (km) [Mặc định]")
            print("     2. Theo Thời gian giờ cao điểm tránh tắc đường (phút)")
            m_choice = input("   Chọn chế độ (1/2, mặc định 1): ").strip()
            mode = "time_peak" if m_choice == "2" else "distance"
            delivery_service.find_shortest_delivery_route(start, dest, mode=mode)

        elif choice == "2":
            delivery_service.process_pending_orders_by_priority()

        elif choice == "3":
            ConsoleView.print_section("3. TỐI ƯU HÓA TẢI TRỌNG XE MÁY SHIPPER (0/1 KNAPSACK)")
            cap_input = input("-> Nhập tải trọng tối đa của xe máy Shipper (kg) [Mặc định: 25.0]: ").strip()
            capacity = float(cap_input) if cap_input else 25.0
            hub_input = input("-> Nhập mã bưu cục lấy hàng (VD: 'CG', 'TX', 'HK') [Mặc định: 'CG']: ").strip()
            hub_id = hub_input if hub_input else "CG"
            delivery_service.optimize_shipper_package_loading(capacity, hub_id)

        elif choice == "4":
            ConsoleView.print_section("4. LẬP LỘ TRÌNH GIAO ĐA ĐIỂM (TSP SOVLER)")
            hub_input = input("-> Nhập Hub xuất phát (VD: 'Cau Giay', 'CG') [Mặc định: 'CG']: ").strip()
            hub = hub_input if hub_input else "CG"
            print("-> Nhập các quận cần giao (cách nhau bởi dấu phẩy)")
            print("   Ví dụ: Ba Dinh, Hoan Kiem, Dong Da, Hai Ba Trung")
            pts_input = input("   Các điểm giao: ").strip()
            if pts_input:
                stops = [p.strip() for p in pts_input.split(",") if p.strip()]
            else:
                stops = ["BD", "HK", "DD"]
                print("   [!] Sử dụng mặc định: Ba Dinh, Hoan Kiem, Dong Da")
            delivery_service.plan_multi_stop_delivery(hub, stops)

        elif choice == "5":
            ConsoleView.print_section("5. TRA CỨU ĐƠN HÀNG BẰNG BẢNG BĂM (HASH TABLE)")
            print("Gợi ý mã đơn mẫu: HN_ORD_101, HN_ORD_102, HN_ORD_105, HN_ORD_108, HN_ORD_115")
            order_id = input("-> Nhập mã vận đơn cần tra cứu: ").strip()
            delivery_service.lookup_order(order_id)

        elif choice == "6":
            ConsoleView.print_section("6. GỢI Ý ĐỊA DANH / TỰ ĐỘNG HOÀN THÀNH (TRIE)")
            prefix = input("-> Nhập tiền tố tìm kiếm (VD: 'Ba', 'Ha', 'Dong', 'Cau', 'B'): ").strip()
            delivery_service.autocomplete_district(prefix)

        elif choice == "7":
            handle_show_data(map_service, delivery_service)

        elif choice == "8":
            delivery_service.run_all_test_benchmarks()

        elif choice == "0":
            print("\n[+] Cảm ơn bạn đã sử dụng hệ thống")
            break
        else:
            print("[!] Lựa chọn không hợp lệ, vui lòng chọn số từ 0 đến 8.")

        input("\n[Nhấn Enter để quay về Menu chính...]")

if __name__ == "__main__":
    main()
