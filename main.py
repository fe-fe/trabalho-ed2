import os
import time


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
            
                
if __name__ == "__main__":
    freq_dict = dict()
    for c in get_binary_file_stream("test.txt", 1):
        get_chunk_byte_frequency(c, freq_dict)
        
    for item in freq_dict.items():
        print(f"char: {bytes([item[0]]).decode()} freq: {item[1]}")