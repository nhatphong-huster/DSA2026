# HỆ THỐNG GIAO HÀNG THÔNG MINH NỘI THÀNH HÀ NỘI (H-LOGISTICS)
> **Đồ Án Môn Học:** Cấu Trúc Dữ Liệu và Giải Thuật (Data Structures and Algorithms - DSA)  
> **Chủ đề:** Giao hàng logistics nội thành (12 Quận nội thành Thủ đô Hà Nội)  
> **Ngôn ngữ:** Python 3 (100% Cài đặt DSA thuần, không sử dụng thư viện ngoài có sẵn)

---

## 📌 1. TỔNG QUAN DỰ ÁN

Dự án mô phỏng và giải quyết các bài toán cốt lõi trong chuỗi vận hành logistics đô thị tại 12 quận nội thành Hà Nội:
* **Không gian mạng lưới:** 12 quận (*Ba Đình, Hoàn Kiếm, Đống Đa, Hai Bà Trưng, Cầu Giấy, Thanh Xuân, Tây Hồ, Hoàng Mai, Long Biên, Nam Từ Liêm, Bắc Từ Liêm, Hà Đông*) với các Hub bưu cục trung tâm và các trục đường huyết mạch (Nguyễn Trãi, Kim Mã, Cầu Giấy, Giải Phóng, Vành đai 2, Vành đai 3, cầu Vĩnh Tuy, cầu Chương Dương, cầu Nhật Tân,...).
* **Mục tiêu:** Ánh xạ các nghiệp vụ thực tế thành các cấu trúc dữ liệu và giải thuật kinh điển nhằm đạt hiệu quả tối ưu về thời gian và chi phí vận chuyển.

---

## 💡 2. BẢNG ÁNH XẠ NGHIỆP VỤ & CẤU TRÚC DỮ LIỆU - GIẢI THUẬT

| Nghiệp vụ Logistics | Cấu trúc Dữ liệu (DSA) | Giải thuật (Algorithm) | Độ phức tạp | File mã nguồn |
| :--- | :--- | :--- | :--- | :--- |
| **Mạng lưới giao thông các quận** | **Graph (Đồ thị có trọng số)**: Danh sách kề (Adjacency List) | Biểu diễn đồ thị vô hướng | Lưu trữ: $O(V + E)$ | [`src/dsa/graph.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/dsa/graph.py) |
| **Tìm tuyến giao nhanh/ngắn nhất** | Đồ thị kết hợp **Min-Heap** | **Dijkstra** (theo cự ly km hoặc thời gian giờ cao điểm) | $O((V + E) \log V)$ | [`src/algorithms/dijkstra.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/algorithms/dijkstra.py) |
| **Điều phối đơn hàng theo mức ưu tiên** | **Priority Queue (Binary Heap)** tự xây dựng từ đầu | Heapify, Sift-Up, Sift-Down | Thêm/Lấy: $O(\log N)$ | [`src/dsa/priority_queue.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/dsa/priority_queue.py) |
| **Tối ưu sức chứa xe máy Shipper** | Mảng Quy hoạch động (DP Table) | **Quy hoạch động 0/1 Knapsack** (tối đa cước phí không quá tải) | $O(N \cdot W)$ | [`src/algorithms/knapsack.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/algorithms/knapsack.py) |
| **Lập lộ trình giao đa điểm cho Shipper** | Đồ thị & Ma trận chi phí | **TSP Solver** bằng **Greedy Nearest Neighbor** | $O(K^2 \cdot (V+E)\log V)$ | [`src/algorithms/tsp_solver.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/algorithms/tsp_solver.py) |
| **Tra cứu nhanh mã vận đơn tức thời** | **Hash Table (Bảng băm)** với Separate Chaining & Auto-Rehashing | Hàm băm đa thức (Polynomial Hash) modulo số nguyên tố | Trung bình: $O(1)$ | [`src/dsa/hash_table.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/dsa/hash_table.py) |
| **Tìm kiếm gợi ý địa danh / bưu cục** | **Cây tiền tố (Trie - Prefix Tree)** | Trie Search & Autocomplete DFS | $O(L)$ ($L$ là độ dài từ) | [`src/dsa/trie.py`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/src/dsa/trie.py) |

---

## 📂 3. CẤU TRÚC DỰ ÁN

```text
DSA2026/
│
├── data/
│   ├── hanoi_districts.json     # 12 quận nội thành, tọa độ, Hub trung chuyển, mật độ giao thông
│   ├── hanoi_graph.json         # Danh sách cạnh đồ thị (khoảng cách km, thời gian thường, cao điểm)
│   └── sample_orders.json       # 15 đơn hàng mẫu phong phú về mức ưu tiên và khối lượng
│
├── src/
│   ├── models/
│   │   ├── district.py          # Class District (quận, bưu cục)
│   │   ├── order.py             # Class Order (đơn hàng, hàm so sánh __lt__ cho Heap)
│   │   └── shipper.py           # Class Shipper (tải trọng xe máy, trạng thái đơn)
│   │
│   ├── dsa/                     # CORE CẤU TRÚC DỮ LIỆU TỰ CÀI ĐẶT THUẦN
│   │   ├── graph.py             # Đồ thị Danh sách kề (Adjacency List) & Edge
│   │   ├── priority_queue.py    # Binary Heap (Hỗ trợ Min-Heap và Max-Heap từ đầu)
│   │   ├── hash_table.py        # Bảng băm có xử lý va chạm Chaining và tự dãn bảng Rehashing
│   │   └── trie.py              # Cây tiền tố phục vụ Autocomplete địa danh
│   │
│   ├── algorithms/              # CORE GIẢI THUẬT TỐI ƯU
│   │   ├── dijkstra.py          # Thuật toán tìm đường ngắn nhất (kết hợp Min-Heap)
│   │   ├── knapsack.py          # Thuật toán 0/1 Knapsack quy hoạch động (xử lý số thực)
│   │   └── tsp_solver.py        # Thuật toán Nearest Neighbor cho bài toán TSP giao đa điểm
│   │
│   ├── services/
│   │   ├── map_service.py       # Quản lý đồ thị bản đồ và tìm kiếm địa danh
│   │   └── delivery_service.py  # Điều phối toàn bộ nghiệp vụ, tích hợp các thuật toán
│   │
│   └── utils/
│       └── console_view.py      # Tiện ích in bảng biểu ASCII, format CLI trực quan
│
├── tests/
│   └── run_tests.py             # Unit test tự động kiểm thử độc lập từng module DSA (100% Pass)
│
├── main.py                      # FILE CHẠY CHÍNH TOÀN BỘ HỆ THỐNG (Interactive CLI)
└── README.md                    # Tài liệu hướng dẫn đồ án
```

---

## 🚀 4. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH

### Yêu cầu môi trường:
* Python 3.8+ (Chạy được ngay trên mọi hệ điều hành Windows, macOS, Linux mà **không cần cài thêm bất kỳ thư viện ngoài nào (no pip install needed)**).

### 1. Chạy chương trình giao diện điều khiển chính:
Mở terminal tại thư mục dự án và chạy:
```bash
python main.py
```

**Các tùy chọn trên Menu tương tác:**
* **Phím 1:** Tìm tuyến đường ngắn nhất giữa 2 quận (Dijkstra theo km hoặc theo thời gian giờ cao điểm).
* **Phím 2:** Lấy đơn hàng từ Hàng đợi ưu tiên (Heap Dispatch) - Hỏa tốc (Level 3) luôn ra trước Tiêu chuẩn (Level 1).
* **Phím 3:** Tối ưu hóa tải trọng hàng xếp lên xe máy của Shipper (0/1 Knapsack Dynamic Programming).
* **Phím 4:** Lập lộ trình giao đa điểm khép vòng về Hub cho Shipper (TSP Nearest Neighbor).
* **Phím 5:** Tra cứu mã vận đơn tức thời trong thời gian thực $O(1)$ bằng Bảng băm (Hash Table).
* **Phím 6:** Gợi ý tìm kiếm quận / Hub bưu cục bằng Cây tiền tố (Trie Autocomplete).
* **Phím 7:** Xem toàn bộ danh sách 12 quận và đơn hàng mẫu.
* **Phím 8:** Chạy bộ kiểm thử tự động toàn diện (Automated Benchmark Suite).
* **Phím 0:** Thoát chương trình.

### 2. Chạy bộ Unit Tests kiểm thử độc lập:
```bash
python tests/run_tests.py
```
Toàn bộ 6/6 test cases của `Graph`, `PriorityQueue`, `HashTable`, `Trie`, `Knapsack` và `Dijkstra` sẽ được kiểm tra với kết quả `PASSED 100%`.

---

## 🎯 5. HƯỚNG DẪN TÙY CHỈNH DỮ LIỆU ĐỒ ÁN

Bạn có thể dễ dàng thay đổi dữ liệu trong thư mục `data/` mà không cần sửa code:
1. **Thay đổi khoảng cách / tuyến đường:** Sửa file [`data/hanoi_graph.json`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/data/hanoi_graph.json).
2. **Thêm/bớt đơn hàng, chỉnh cước phí, khối lượng, mức ưu tiên:** Sửa file [`data/sample_orders.json`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/data/sample_orders.json).
3. **Thêm/sửa địa chỉ bưu cục các quận:** Sửa file [`data/hanoi_districts.json`](file:///c:/Users/FPTSHOP/Desktop/DSA2026/data/hanoi_districts.json).
