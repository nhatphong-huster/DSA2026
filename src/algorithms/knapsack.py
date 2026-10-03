"""
Thuật toán Quy hoạch động 0/1 Knapsack (Bài toán chiếc ba lô).
Áp dụng: Tối ưu hóa việc chọn tập đơn hàng để chất lên xe máy của Shipper sao cho
tổng cước phí thu được là lớn nhất mà không vượt quá tải trọng cho phép của xe máy (W kg).
Độ phức tạp: O(N * W) với N là số đơn, W là tải trọng xe.
"""

def solve_knapsack_01(orders: list, max_capacity_kg: float, scale_factor: int = 10):
    """
    Quy hoạch động 0/1 Knapsack xử lý được số thực (thông qua nhân tỉ lệ scale_factor).
    
    Tham số:
    - orders: Danh sách các đối tượng Order (mỗi order có weight_kg và shipping_fee_vnd).
    - max_capacity_kg: Tải trọng tối đa xe máy (kg).
    - scale_factor: Hệ số quy đổi số thực sang số nguyên (10 nghĩa là chính xác tới 0.1 kg).

    Trả về:
    - dict kết quả: selected_orders, total_weight_kg, total_fee_vnd, remaining_capacity_kg, dp_table_shape
    """
    if not orders or max_capacity_kg <= 0:
        return {
            "selected_orders": [],
            "total_weight_kg": 0.0,
            "total_fee_vnd": 0,
            "remaining_capacity_kg": max_capacity_kg
        }

    n = len(orders)
    # Quy đổi tải trọng và khối lượng sang số nguyên
    scaled_capacity = int(round(max_capacity_kg * scale_factor))
    scaled_weights = [int(round(order.weight_kg * scale_factor)) for order in orders]
    values = [int(order.shipping_fee_vnd) for order in orders]

    # Khởi tạo bảng quy hoạch động dp[i][w]
    # dp[i][w]: Giá trị cước lớn nhất khi xét i đơn hàng đầu tiên với sức chứa w
    dp = [[0] * (scaled_capacity + 1) for _ in range(n + 1)]

    # Bước 1: Xây dựng bảng quy hoạch động từ dưới lên (Bottom-up)
    for i in range(1, n + 1):
        w = scaled_weights[i - 1]
        v = values[i - 1]
        for cap in range(scaled_capacity + 1):
            if w <= cap:
                dp[i][cap] = max(dp[i - 1][cap], dp[i - 1][cap - w] + v)
            else:
                dp[i][cap] = dp[i - 1][cap]

    # Bước 2: Truy vết tìm lại danh sách các đơn hàng đã được chọn
    selected_orders = []
    cap = scaled_capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            # Đơn hàng thứ i-1 đã được chọn
            selected_orders.append(orders[i - 1])
            cap -= scaled_weights[i - 1]

    # Đảo lại thứ tự cho đúng thứ tự ban đầu
    selected_orders.reverse()

    total_fee = dp[n][scaled_capacity]
    total_weight = sum(o.weight_kg for o in selected_orders)
    remaining_capacity = max(0.0, max_capacity_kg - total_weight)

    return {
        "selected_orders": selected_orders,
        "total_weight_kg": round(total_weight, 2),
        "total_fee_vnd": total_fee,
        "remaining_capacity_kg": round(remaining_capacity, 2),
        "dp_matrix_shape": f"({n + 1} x {scaled_capacity + 1})"
    }
