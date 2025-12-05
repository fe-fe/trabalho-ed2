from file_utils import *
import huffman
import json
from datetime import datetime
import argparse
from search_compress import search_in_compressed_file, search_in_compressed_file_with_positions


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compressor de arquivos Huffman")
    
    subparsers = parser.add_subparsers(dest="action", required=True, help="Ação a ser executada")

    parser_compress = subparsers.add_parser("compress", help="Comprimir um arquivo")
    parser_compress.add_argument("arquivo_original", help="Nome do arquivo para processar")
    parser_compress.add_argument("arquivo_destino", help="Nome do arquivo para salvar")

    parser_decompress = subparsers.add_parser("decompress", help="Descomprimir um arquivo")
    parser_decompress.add_argument("arquivo_original", help="Nome do arquivo compactado")
    parser_decompress.add_argument("arquivo_destino", help="Nome do arquivo restaurado")
    
    parser_compare = subparsers.add_parser("compare", help="comparar dois arquivos")
    parser_compare.add_argument("arquivo_um", help="Nome do primeiro arquivo")
    parser_compare.add_argument("arquivo_dois", help="Nome do segundo arquivo")
    
    parser_search = subparsers.add_parser("search", help="Buscar um padrão no arquivo")
    parser_search.add_argument("arquivo_original", help="Nome do arquivo onde buscar")
    parser_search.add_argument("pattern", help="Padrão (texto ou bytes) para buscar")
    parser_search.add_argument("-p", dest="pos", action="store_true", help="faz a busca por matches e posicoes")

    args = parser.parse_args()
    
    
    if args.action == "compare":
        equal = check_decompression(args.arquivo_um, args.arquivo_dois)
        print(f"a decompressao foi {"bem" if equal else "mal"} sucedida!")

    if args.action == "compress":
        huffman.compress_file(args.arquivo_original, args.arquivo_destino)
        
    elif args.action == "decompress":
        huffman.decompress_file(args.arquivo_original, args.arquivo_destino)

    elif args.action == "search":
        
        search_bytes = args.pattern.encode()
        print("\nBuscando substring no arquivo comprimido...")
        
        if not args.pos:
            busca = search_in_compressed_file(args.arquivo_original, search_bytes)
            if busca:
                print(f"\n : ) Encontrou '{args.pattern}' dentro do arquivo comprimido!")
            else:
                print(f"\n : ( NÃO encontrou '{args.pattern}' dentro do arquivo comprimido.")
        else:
            posicoes = search_in_compressed_file_with_positions(args.arquivo_original, search_bytes)
            if posicoes:
                print("Encontrado nas posições:", posicoes)
            else:
                print("Não encontrado.")