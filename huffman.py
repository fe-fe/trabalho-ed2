import pickle
import os
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
    
    if not freq_items:
        return None
    if len(freq_items) == 1:
        node = Node.from_tuple(freq_items[0])
        return Node.from_edges(node, Node.from_tuple((None, 0)))

    edges = [Node.from_tuple(item) for item in freq_items]
    
    while True:
        left = edges[1]
        right = edges[0]
        node = Node.from_edges(left, right)
        edges = edges[2:]
        if len(edges) > 0:
            edges.insert(0, node)
            edges.sort(key=lambda x: x.freq)
        else:
            break
        
    return node


def get_codes(node: Node, code_dict: dict, current: str) -> dict[str, str]:
    if not node:
        return
    
    if node.is_leaf():
        code_dict[node.byte] = current if current else "0"
        return
    
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
    freq_dict = dict()
    for chunk in get_binary_file_stream(file_path, 1024):
        get_stream_byte_frequency(chunk, freq_dict)
    
    if not freq_dict:
        print("Empty file, skipping compression.")
        return

    tree = build_huffman_frequency_tree(freq_dict)
    code_dict = dict()
    get_codes(tree, code_dict, str())
    
    with open(compressed_file_path, "wb") as file_out:
        pickle.dump(freq_dict, file_out)
        
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
        
        padding = 0
        if len(buffer_str) > 0:
            padding = 8 - len(buffer_str)
            buffer_str += "0" * padding
            final_byte = int(buffer_str, 2)
            file_out.write(bytes([final_byte]))
        
        file_out.write(bytes([padding]))


def decompress_bit_string(bits_string: str, current_node: Node, tree_root: Node) -> tuple[bytearray, Node]:
    """
    Decodes a string of bits (e.g. "10110") into bytes.
    Returns:
       - The decoded bytes found so far.
       - The Node where we stopped (to continue next time).
    """
    decoded_data = bytearray()
    node = current_node
    
    for bit in bits_string:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        
        if node.is_leaf():
            # FIXED: Used append() instead of extend() because node.byte is an int
            decoded_data.append(node.byte)
            node = tree_root
            
    return decoded_data, node


def decompress_file(file_path: str) -> None:
    decompressed_path = file_path.replace("_compressed", "_restored")
    if decompressed_path == file_path:
        decompressed_path += "_restored"

    with open(file_path, "rb") as file_in:
        try:
            freq_dict = pickle.load(file_in)
        except EOFError:
            print("Empty or invalid compressed file.")
            return

        tree = build_huffman_frequency_tree(freq_dict)

        with open(decompressed_path, "wb") as file_out:
            current_node = tree
            current_chunk = file_in.read(1024)
            
            while True:
                next_chunk = file_in.read(1024)

                if next_chunk:
                    bits = ""
                    for byte_val in current_chunk:
                        bits += format(byte_val, '08b')
                        
                    data, current_node = decompress_bit_string(bits, current_node, tree)
                    file_out.write(data)
                    
                    current_chunk = next_chunk
                
                else:
                    if len(current_chunk) == 0:
                        break

                    padding_byte = current_chunk[-1]
                    data_part = current_chunk[:-1]
                    
                    bits = ""
                    for byte_val in data_part:
                        bits += format(byte_val, '08b')
                    
                    if padding_byte > 0:
                        bits = bits[:-padding_byte]
                        
                    data, current_node = decompress_bit_string(bits, current_node, tree)
                    file_out.write(data)

                    if current_node != tree:
                        print("não encontrou a ultima correspondencia")
                    break