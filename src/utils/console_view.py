"""
Tiện ích hiển thị giao diện dòng lệnh (CLI Visualizer & Formatter).
Tạo bảng biểu ASCII, phân cách và format trực quan cho đồ án DSA.
"""

class ConsoleView:
    @staticmethod
    def print_header(title: str, width: int = 75):
        print("\n" + "=" * width)
        print(f" {title.upper()} ".center(width, "="))
        print("=" * width)

    @staticmethod
    def print_section(title: str, width: int = 75):
        print("\n" + "-" * width)
        print(f"[*] {title}")
        print("-" * width)

    @staticmethod
    def print_order_table(orders: list):
        """In danh sách đơn hàng dạng bảng đẹp mắt."""
        if not orders:
            print("[!] Không có đơn hàng nào trong danh sách.")
            return

        header = f"{'MÃ ĐƠN':<12} | {'TỪ -> ĐẾN':<12} | {'LOẠI HÀNG':<22} | {'KL (kg)':<8} | {'CƯỚC (đ)':<10} | {'MỨC ƯU TIÊN':<15}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        for o in orders:
            route = f"{o.sender_district} -> {o.receiver_district}"
            pkg = (o.package_type[:20] + "..") if len(o.package_type) > 22 else o.package_type
            p_text = f"L{o.priority_level} ({o.priority_name.split()[0]})"
            print(f"{o.order_id:<12} | {route:<12} | {pkg:<22} | {o.weight_kg:<8.1f} | {o.shipping_fee_vnd:<10,}"
                  f" | {p_text:<15}")

        print("-" * len(header))
        print(f"Tổng số đơn: {len(orders)} | Tổng khối lượng: {sum(o.weight_kg for o in orders):.1f} kg | "
              f"Tổng tiền cước: {sum(o.shipping_fee_vnd for o in orders):,} VNĐ\n")

    @staticmethod
    def print_route_summary(start: str, end: str, cost: float, path: list, edges: list, mode: str = "distance"):
        """In tóm tắt lộ trình tìm kiếm bởi Dijkstra."""
        print(f"\n[+] Lộ trình tối ưu từ [{start}] đến [{end}]:")
        path_str = "  ==>  ".join(path)
        print(f"    Tuyến đường: {path_str}")

        if mode == "distance":
            print(f"    Tổng khoảng cách: {cost:.2f} km")
            total_time = sum(e.base_time_min for e in edges)
            print(f"    Thời gian di chuyển ước tính (giờ thường): ~{total_time} phút")
            total_peak = sum(e.peak_time_min for e in edges)
            print(f"    Thời gian di chuyển giờ cao điểm (tắc đường): ~{total_peak} phút")
        else:
            print(f"    Tổng thời gian: {cost:.1f} phút")

        if edges:
            print("\n    [Chi tiết từng chặng đường]:")
            for i, e in enumerate(edges, 1):
                prev_node = path[i - 1]
                print(f"      {i}. {prev_node} -> {e.neighbor}: {e.distance_km}km ({e.base_time_min}p) [{e.route_name}]")
