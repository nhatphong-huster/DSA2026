"""
Unit tests kiểm thử độc lập từng Cấu trúc dữ liệu và Giải thuật cốt lõi.
Chạy trực tiếp: python tests/run_tests.py
"""
import sys
import os

# Thêm thư mục gốc vào PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dsa.graph import Graph
from src.dsa.priority_queue import PriorityQueue
from src.dsa.hash_table import HashTable
from src.dsa.trie import Trie
from src.algorithms.dijkstra import dijkstra_shortest_path
from src.algorithms.knapsack import solve_knapsack_01
from src.algorithms.tsp_solver import solve_multi_stop_delivery
from src.models.order import Order

def test_graph():
    print("[*] Testing Graph...")
    g = Graph()
    g.add_edge("A", "B", 5.0, 10, 20, "Tuyến A-B")
    g.add_edge("B", "C", 3.0, 8, 15, "Tuyến B-C")
    assert g.num_vertices == 3
    assert g.num_edges == 2
    neighbors = [e.neighbor for e in g.get_neighbors("B")]
    assert "A" in neighbors and "C" in neighbors
    print("    -> Graph: PASSED")

def test_priority_queue():
    print("[*] Testing PriorityQueue (Min-Heap & Max-Heap)...")
    # Min-Heap
    min_pq = PriorityQueue(is_min_heap=True)
    for val in [15, 3, 8, 1, 20, 2]:
        min_pq.push(val)
    sorted_min = [min_pq.pop() for _ in range(6)]
    assert sorted_min == [1, 2, 3, 8, 15, 20]

    # Max-Heap
    max_pq = PriorityQueue(is_min_heap=False)
    for val in [15, 3, 8, 1, 20, 2]:
        max_pq.push(val)
    sorted_max = [max_pq.pop() for _ in range(6)]
    assert sorted_max == [20, 15, 8, 3, 2, 1]
    print("    -> PriorityQueue: PASSED")

def test_hash_table():
    print("[*] Testing HashTable (with collisions & rehashing)...")
    ht = HashTable(capacity=5) # Kích thước nhỏ để kích hoạt collision và rehashing
    for i in range(20):
        ht.put(f"key_{i}", f"val_{i}")
    assert len(ht) == 20
    assert ht.get("key_7") == "val_7"
    assert ht.get("key_19") == "val_19"
    assert ht.remove("key_7") is True
    assert ht.get("key_7") is None
    assert len(ht) == 19
    print("    -> HashTable: PASSED")

def test_trie():
    print("[*] Testing Trie...")
    trie = Trie()
    trie.insert("Cau Giay", "CG")
    trie.insert("Ba Dinh", "BD")
    trie.insert("Bac Tu Liem", "BTL")
    assert trie.search("Cau Giay") is True
    assert trie.search("Hoan Kiem") is False
    res_b = trie.autocomplete("Ba")
    assert len(res_b) == 2  # Ba Dinh & Bac Tu Liem
    print("    -> Trie: PASSED")

def test_knapsack():
    print("[*] Testing 0/1 Knapsack Dynamic Programming...")
    orders = [
        Order("ORD1", "", "A", "", "", "B", "", "P1", weight_kg=6, shipping_fee_vnd=60000),
        Order("ORD2", "", "A", "", "", "B", "", "P2", weight_kg=10, shipping_fee_vnd=120000),
        Order("ORD3", "", "A", "", "", "B", "", "P3", weight_kg=8, shipping_fee_vnd=90000),
        Order("ORD4", "", "A", "", "", "B", "", "P4", weight_kg=12, shipping_fee_vnd=130000)
    ]
    # Sức chứa 20kg -> Tối ưu là ORD3 (8kg, 90k) + ORD4 (12kg, 130k) = 20kg, 220k
    res = solve_knapsack_01(orders, max_capacity_kg=20.0)
    assert res["total_fee_vnd"] == 220000
    assert res["total_weight_kg"] == 20.0
    selected_ids = [o.order_id for o in res["selected_orders"]]
    assert "ORD3" in selected_ids and "ORD4" in selected_ids
    print("    -> Knapsack: PASSED")

def test_dijkstra():
    print("[*] Testing Dijkstra Algorithm...")
    g = Graph()
    g.add_edge("A", "B", 4.0)
    g.add_edge("A", "C", 2.0)
    g.add_edge("C", "B", 1.0)
    g.add_edge("B", "D", 5.0)
    g.add_edge("C", "D", 8.0)
    # A -> C -> B -> D: 2 + 1 + 5 = 8.0
    cost, path, _ = dijkstra_shortest_path(g, "A", "D")
    assert cost == 8.0
    assert path == ["A", "C", "B", "D"]
    print("    -> Dijkstra: PASSED")

def run_all():
    print("=" * 60)
    print(" BẮT ĐẦU CHẠY UNIT TEST TOÀN BỘ CÁC MODULE DSA")
    print("=" * 60)
    test_graph()
    test_priority_queue()
    test_hash_table()
    test_trie()
    test_knapsack()
    test_dijkstra()
    print("=" * 60)
    print(" TẤT CẢ UNIT TESTS ĐÃ VƯỢT QUA 100%!")
    print("=" * 60)

if __name__ == "__main__":
    run_all()
