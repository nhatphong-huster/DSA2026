"""
Cài đặt Cây tiền tố (Trie) để tìm kiếm và tự động gợi ý (Autocomplete)
địa danh, quận huyện và Hub bưu cục.
"""

class TrieNode:
    """Một nút trên cây tiền tố Trie."""
    def __init__(self):
        self.children = {}            # Ký tự tiếp theo -> TrieNode
        self.is_end_of_word = False   # Đánh dấu kết thúc một từ
        self.payload = []             # Dữ liệu đính kèm (VD: Object District)


class Trie:
    """
    Cây tiền tố (Prefix Tree)
    - Thao tác Insert: O(L) với L là độ dài từ.
    - Thao tác Search: O(L).
    - Thao tác Autocomplete: O(P + K) với P là độ dài prefix, K là số nút trong cây con.
    """
    def __init__(self):
        self.root = TrieNode()

    def _normalize(self, text: str) -> str:
        """Chuyển về chữ thường để tìm kiếm không phân biệt hoa thường."""
        return text.strip().lower()

    def insert(self, word: str, data=None):
        """
        Thêm một từ vào cây Trie kèm dữ liệu liên kết.
        Độ phức tạp: O(L)
        """
        node = self.root
        normalized_word = self._normalize(word)

        for char in normalized_word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        node.is_end_of_word = True
        if data is not None:
            node.payload.append((word, data))
        else:
            node.payload.append((word, None))

    def search(self, word: str) -> bool:
        """
        Kiểm tra từ có tồn tại chính xác trong Trie hay không.
        Độ phức tạp: O(L)
        """
        node = self.root
        normalized_word = self._normalize(word)

        for char in normalized_word:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.is_end_of_word

    def autocomplete(self, prefix: str) -> list:
        """
        Tìm tất cả các từ và dữ liệu có tiền tố bắt đầu bằng prefix.
        Độ phức tạp: O(P + K)
        """
        results = []
        node = self.root
        normalized_prefix = self._normalize(prefix)

        # 1. Duyệt đến nút kết thúc của prefix
        for char in normalized_prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        # 2. Duyệt đệ quy DFS thu thập toàn bộ các từ trong cây con
        self._dfs_collect(node, results)
        return results

    def _dfs_collect(self, node: TrieNode, results: list):
        if node.is_end_of_word:
            for item in node.payload:
                results.append(item)

        for char, child_node in node.children.items():
            self._dfs_collect(child_node, results)

    def __repr__(self):
        return "Trie(Prefix Tree for District Autocomplete)"
