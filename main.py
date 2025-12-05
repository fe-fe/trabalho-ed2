from file_utils import *
import huffman
import json
from datetime import datetime

from search_compress import search_in_compressed_file, search_in_compressed_file_with_positions


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

    
    search_word = input("\nDigite a palavra que deseja buscar no arquivo comprimido: ").strip()
    search_bytes = search_word.encode()

    # Buscar no arquivo comprimido
    print("\nBuscando substring no arquivo comprimido...")
    busca = search_in_compressed_file("test_compressed.txt", search_bytes)

    if busca:
        print(f"\n : ) Encontrou '{search_word}' dentro do arquivo comprimido!")
    else:
        print(f"\n : ( NÃO encontrou '{search_word}' dentro do arquivo comprimido.")

    #busca em arquivo comprimido retornando offset em arquivo original
    search_word = input("\nDigite a palavra que deseja buscar no arquivo comprimido: ").strip()
    search_bytes = search_word.encode()

    posicao = search_in_compressed_file_with_positions("test_compressed.txt", search_bytes)

    if posicao:
        print("Encontrado nas posições:", posicao)
    else:
        print("Não encontrado.")