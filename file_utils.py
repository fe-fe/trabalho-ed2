import os
import filecmp

def get_binary_file_stream(file_path: str, chunk_bytes: int = 100):
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_bytes)
            if chunk:
                yield chunk
            else:
                break


def create_file(file_path: str):
    with open(file_path, "wb") as f:
        pass


def append_to_binary_file(file_path: str, chunk: bytes):
    with open(file_path, "ab") as f:
        f.write(chunk)   
        
        
def build_compressed_file_name(file_path: str) -> str:
    file, extension = os.path.splitext(file_path)
    file += "_compressed"
    return file + extension


def check_decompression(original_path, decompressed_path) -> bool:
    return filecmp.cmp(original_path, decompressed_path)