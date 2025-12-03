from binary_tree import Node


def get_stream_byte_frequency(chunk: bytes, freq_dict: dict):
    for byte in chunk:
        freq_dict[byte] = freq_dict.get(byte, 0) + 1
    return freq_dict        
        
                
def build_huffman_frequency_tree(freq_dict: dict) -> Node:
    freq_items = sorted(
        freq_dict.items(),
        key=lambda item: item[1],
        reverse=False
    )
    
    edges = [Node.from_tuple(item) for item in freq_items]
    
    while True:
        left = edges[1]
        right = edges[0]
        node = Node.from_edges(left, right)
        edges = edges[2:]
        if len(edges) > 0:
            edges.insert(0, node)
        else:
            break
        
    return node


def get_codes(node: Node, code_list: list, current: str) -> list[tuple[bytes, str]]: # (data, code)
    
    if not node:
        return
    
    if node.is_leaf():
        code_list.append(
            (node.byte, current)
        )
    
    get_codes(node.left, code_list, current + "0")
    get_codes(node.right, code_list, current + "1")
    
    return code_list