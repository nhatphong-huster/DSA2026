"""
Cài đặt Hàng đợi ưu tiên (Priority Queue) thuần từ đầu bằng Cấu trúc Min/Max Binary Heap.
Không sử dụng thư viện heapq của Python.
"""

class PriorityQueue:
    """
    Binary Heap hỗ trợ cả Min-Heap và Max-Heap.
    - Mặc định: is_min_heap = True (Giá trị nhỏ nhất/ưu tiên cao nhất ở gốc).
    - Thao tác Push: O(log N)
    - Thao tác Pop: O(log N)
    - Thao tác Peek: O(1)
    """
    def __init__(self, is_min_heap: bool = True):
        self.heap = []
        self.is_min_heap = is_min_heap

    def _should_swap(self, child_val, parent_val) -> bool:
        """Kiểm tra điều kiện hoán vị dựa trên tính chất Heap."""
        if self.is_min_heap:
            return child_val < parent_val
        else:
            return child_val > parent_val

    def push(self, item):
        """
        Thêm một phần tử vào heap và duy trì thuộc tính heap bằng cách sift-up.
        Độ phức tạp thời gian: O(log N)
        """
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """
        Lấy và loại bỏ phần tử ở đỉnh heap (nhỏ nhất hoặc lớn nhất).
        Độ phức tạp thời gian: O(log N)
        """
        if self.is_empty():
            raise IndexError("Hàng đợi ưu tiên đang rỗng!")

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        # Đưa phần tử cuối lên gốc và sift-down
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def peek(self):
        """
        Xem phần tử ở đỉnh mà không lấy ra khỏi heap.
        Độ phức tạp thời gian: O(1)
        """
        if self.is_empty():
            raise IndexError("Hàng đợi ưu tiên đang rỗng!")
        return self.heap[0]

    def _sift_up(self, index: int):
        """Đẩy phần tử tại vị trí index lên trên cây nhị phân để thỏa mãn Heap."""
        while index > 0:
            parent_idx = (index - 1) // 2
            if self._should_swap(self.heap[index], self.heap[parent_idx]):
                self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
                index = parent_idx
            else:
                break

    def _sift_down(self, index: int):
        """Hạ phần tử tại vị trí index xuống dưới cây nhị phân để thỏa mãn Heap."""
        size = len(self.heap)
        while True:
            target_idx = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2

            if left_child < size and self._should_swap(self.heap[left_child], self.heap[target_idx]):
                target_idx = left_child

            if right_child < size and self._should_swap(self.heap[right_child], self.heap[target_idx]):
                target_idx = right_child

            if target_idx != index:
                self.heap[index], self.heap[target_idx] = self.heap[target_idx], self.heap[index]
                index = target_idx
            else:
                break

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)

    def to_list(self):
        """Trả về bản sao mảng heap hiện tại."""
        return list(self.heap)

    def __len__(self):
        return len(self.heap)

    def __repr__(self):
        heap_type = "MinHeap" if self.is_min_heap else "MaxHeap"
        return f"{heap_type}(size={len(self.heap)})"
