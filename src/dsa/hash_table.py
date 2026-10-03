"""
Cài đặt Bảng băm (Hash Table) thuần từ đầu để tra cứu đơn hàng O(1).
Xử lý xung đột (Collision Resolution) bằng phương pháp Separate Chaining (Nối chuỗi).
Tự động dãn bảng (Rehashing) khi hệ số đầy (Load Factor) >= 0.75.
"""

class HashNode:
    """Nút lưu trữ cặp key-value trong bucket."""
    def __init__(self, key: str, value):
        self.key = key
        self.value = value
        self.next = None

    def __repr__(self):
        return f"Node({self.key} => {self.value})"


class HashTable:
    """
    Bảng băm tùy biến:
    - Tìm kiếm (Get): O(1) trung bình, O(N) xấu nhất khi va chạm toàn bộ.
    - Thêm (Put): O(1) trung bình.
    - Xóa (Remove): O(1) trung bình.
    """
    INITIAL_CAPACITY = 17  # Chọn số nguyên tố ban đầu để giảm thiểu xung đột
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, capacity: int = INITIAL_CAPACITY):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.collision_count = 0

    def _hash_function(self, key: str) -> int:
        """
        Hàm băm đa thức (Polynomial Rolling Hash) kết hợp modulo số nguyên tố.
        h = sum(ord(c) * 31^i) mod capacity
        """
        hash_val = 0
        prime = 31
        for char in str(key):
            hash_val = (hash_val * prime + ord(char)) % self.capacity
        return hash_val

    def put(self, key: str, value):
        """
        Thêm hoặc cập nhật cặp key-value vào bảng băm.
        Độ phức tạp: O(1) trung bình
        """
        index = self._hash_function(key)
        head = self.buckets[index]

        # Kiểm tra nếu key đã tồn tại trong bucket -> Cập nhật value
        curr = head
        while curr is not None:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next

        # Nếu chưa có -> Tạo node mới thêm vào đầu bucket
        if head is not None:
            self.collision_count += 1

        new_node = HashNode(key, value)
        new_node.next = head
        self.buckets[index] = new_node
        self.size += 1

        # Kiểm tra điều kiện dãn bảng (Rehashing)
        if self.get_load_factor() >= self.LOAD_FACTOR_THRESHOLD:
            self._rehash()

    def get(self, key: str):
        """
        Tìm và trả về giá trị ứng với key. Nếu không có trả về None.
        Độ phức tạp: O(1) trung bình
        """
        index = self._hash_function(key)
        curr = self.buckets[index]
        while curr is not None:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def contains(self, key: str) -> bool:
        """Kiểm tra sự tồn tại của key trong bảng băm."""
        return self.get(key) is not None

    def remove(self, key: str) -> bool:
        """
        Xóa cặp key-value khỏi bảng băm.
        Độ phức tạp: O(1) trung bình
        """
        index = self._hash_function(key)
        curr = self.buckets[index]
        prev = None

        while curr is not None:
            if curr.key == key:
                if prev is None:
                    self.buckets[index] = curr.next
                else:
                    prev.next = curr.next
                self.size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def _rehash(self):
        """
        Tăng gấp đôi kích thước bảng băm khi đầy và băm lại toàn bộ dữ liệu.
        """
        old_buckets = self.buckets
        self.capacity = self._next_prime(self.capacity * 2)
        self.buckets = [None] * self.capacity
        self.size = 0
        self.collision_count = 0

        for head in old_buckets:
            curr = head
            while curr is not None:
                self.put(curr.key, curr.value)
                curr = curr.next

    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _next_prime(self, n: int) -> int:
        while not self._is_prime(n):
            n += 1
        return n

    def get_load_factor(self) -> float:
        """Tính hệ số lấp đầy (Load Factor) = N / Capacity."""
        return self.size / self.capacity

    def keys(self) -> list:
        result = []
        for head in self.buckets:
            curr = head
            while curr:
                result.append(curr.key)
                curr = curr.next
        return result

    def values(self) -> list:
        result = []
        for head in self.buckets:
            curr = head
            while curr:
                result.append(curr.value)
                curr = curr.next
        return result

    def items(self) -> list:
        result = []
        for head in self.buckets:
            curr = head
            while curr:
                result.append((curr.key, curr.value))
                curr = curr.next
        return result

    def __len__(self):
        return self.size

    def __getitem__(self, key):
        val = self.get(key)
        if val is None:
            raise KeyError(f"Key '{key}' không tồn tại trong Bảng băm!")
        return val

    def __setitem__(self, key, value):
        self.put(key, value)

    def __repr__(self):
        return (f"HashTable(Size: {self.size}, Capacity: {self.capacity}, "
                f"LoadFactor: {self.get_load_factor():.2f}, Collisions: {self.collision_count})")
