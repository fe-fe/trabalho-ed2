import os
import time



def get_file_stream(file_path: str, char_bytes: int = 1, char_qtd: int = 100):
    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(char_bytes*char_qtd)
            if chunk:
                yield chunk
                
            else:
                break
            
                
if __name__ == "__main__":
    for c in get_file_stream("test.txt", char_qtd=1):
        print(f"{c}+")