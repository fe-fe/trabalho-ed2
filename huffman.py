from binary_tree import Node
from file_utils import *


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


def get_codes(node: Node, code_dict: dict, current: str) -> dict[str, str]: # (data, code)
    if not node:
        return
    
    if node.is_leaf():
        code_dict[node.byte] = current
    
    get_codes(node.left, code_dict, "0" if not current else current + "0")
    get_codes(node.right, code_dict, "1" if not current else current + "1")
    
    return code_dict


def compress_chunk_bytes(chunk: bytes, code_dict: dict) -> str:
    compressed_chunk = str()
    for byte in chunk:
        encoded_byte = code_dict.get(byte)
        if not encoded_byte:
            raise Exception(f"byte not found in code dictionary: [{byte}]")
        compressed_chunk += encoded_byte
    return compressed_chunk




def compress_file(file_path: str) -> None:
    compressed_file_path = build_compressed_file_name(file_path)
    create_file(compressed_file_path)
    for chunk in get_binary_file_stream(file_path, 1024):
        freq_dict = dict()
        get_stream_byte_frequency(chunk, freq_dict)
    tree = build_huffman_frequency_tree(freq_dict)
    code_dict = dict()
    get_codes(tree, code_dict, str())
    with open(compressed_file_path, "wb") as file_out:
        
        buffer_str = "" 
        for chunk in get_binary_file_stream(file_path, 1024):
            compressed_chunk = compress_chunk_bytes(chunk, code_dict)
            buffer_str += compressed_chunk
            bytes_to_write = bytearray()
            
            while len(buffer_str) >= 8:
                byte_bits = buffer_str[:8]
                buffer_str = buffer_str[8:]
                byte_val = int(byte_bits, 2)
                bytes_to_write.append(byte_val)
        
        
            if len(bytes_to_write) > 0:
                file_out.write(bytes_to_write)
        
        if len(buffer_str) > 0:
            padding = 8 - len(buffer_str)
            buffer_str += "0" * padding
            final_byte = int(buffer_str, 2)
            file_out.write(bytes([final_byte]))
                