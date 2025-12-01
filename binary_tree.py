

class Node:
    byte: bytes
    freq: int
    left: "Node"
    right: "Node"
    

    @staticmethod
    def from_tuple(freq_tuple: tuple) -> "Node":
        node = Node()
        node.byte = bytes([freq_tuple[0]])
        node.freq = freq_tuple[1]
        node.left = None
        node.right = None
        return node
    
    
    @staticmethod
    def from_edges(left_edge: "Node", right_edge: "Node") -> "Node":
        node = Node()
        node.byte = None
        node.left = left_edge
        node.right = right_edge
        node.freq = left_edge.freq + right_edge.freq
        return node
    
    
    def to_dict(self):

        byte_rep = "".join([format(b, "08b") for b in self.byte or []])
        
        
        node = {
            "byte": byte_rep if byte_rep != "" else None,
            "char": self.byte.decode() if self.byte else None,
            "freq": self.freq, 
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }
        return node
    
    
    def __str__(self):
        return f"byte {self.byte}: {self.freq}"