from file_utils import *
import huffman
import json
from datetime import datetime


if __name__ == "__main__":
    
    compression_start = datetime.now()
    huffman.compress_file("test.txt")
    compression_end = datetime.now()
    huffman.decompress_file("test_compressed.txt")
    decompression_end = datetime.now()

    total_comp = compression_end - compression_start
    total_decomp = decompression_end - compression_end

    print(f"levou {total_comp} para comprimir")
    print(f"levou {total_decomp} para descomprimir")
    print(f"levou {total_comp + total_decomp} no total")

    print(f"funcionou: {check_decompression("test.txt", "test_restored.txt")}")