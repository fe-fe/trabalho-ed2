import os
import time
from binary_tree import Node

def get_binary_file_stream(file_path: str, chunk_bytes: int = 100):
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_bytes)
            if chunk:
                yield chunk
            else:
                break

        
def get_chunk_byte_frequency(chunk: bytes, freq_dict: dict):
    for byte in chunk:
        freq_dict[byte] = freq_dict.get(byte, 0) + 1
    return freq_dict        
        
                
def build_huffman_frequency_tree(freq_dict: dict) -> Node:
    freq_items = sorted(
        freq_dict.items(),
        key=lambda item: item[1],
        reverse=True
    )
    edges = [Node.from_tuple(item) for item in freq_items]
    while True:
        
        left = edges[0]
        right = edges[1]
        node = Node.from_edges(left, right)
        edges = edges[2:]
        if len(edges) > 0:
            edges.insert(0, node)
        else:
            break
    return node


if __name__ == "__main__":
    freq_dict = dict()
    for c in get_binary_file_stream("test.txt"):
        get_chunk_byte_frequency(c, freq_dict)
    tree = build_huffman_frequency_tree(freq_dict)
    print(tree.to_dict())