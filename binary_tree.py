

class Node:
    byte: bytes
    freq: int
    left: "Node"
    right: "Node"
    

    @staticmethod
    def from_tuple(freq_tuple: tuple) -> "Node":
        node = Node()
        node.byte = freq_tuple[0]
        node.freq = freq_tuple[1]
        return node
    
    
    @staticmethod
    def from_edges(left_edge: "Node", right_edge: "Node") -> "Node":
        node = Node()
        node.byte = left_edge.byte + right_edge.byte # para nao quebrar o to_dict
        node.left = left_edge
        node.right = right_edge
        node.freq = left_edge.freq + right_edge.freq
        return node
    
    
    def to_dict(self):
        node = {
            self.byte: {
                "freq": self.freq
            }
        } 
        if hasattr(self, "left"):
            node[self.byte]["left"] = self.left.to_dict()
        if hasattr(self, "right"):
            node[self.byte]["right"] = self.right.to_dict()
        return node
    
    def __str__(self):
        return f"byte {self.byte}: {self.freq}"