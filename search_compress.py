import pickle

import huffman

def load_huffman_header(path: str):
    with open(path, "rb") as f:
        freq_dict = pickle.load(f)

        header_end = f.tell()

    tree = huffman.build_huffman_frequency_tree(freq_dict)

    return tree, {"freq_dict": freq_dict, "header_end": header_end}

def decompress_stream(bits: str, current_node, tree):
    decoded_bytes = bytearray()
    node = current_node
    i = 0

    while i < len(bits):#bit a bit
        bit = bits[i]

        if bit == "0":
            node = node.left
        else:
            node = node.right

        
        if node.is_leaf():# Se chegou em um símbolo
            decoded_bytes.append(node.byte)
            node = tree

        i += 1

    # Bits que sobraram e não completaram símbolo
    remaining_bits = bits[i:] if node != tree else ""

    return bytes(decoded_bytes), node, remaining_bits


def search_in_compressed_file(path: str, word: bytes) -> bool:
    tree, metadata = load_huffman_header(path)  
    word = word
    current_node = tree
    remaining_bits = ""
    buffer = b""  # serve para comparar pedaços

    with open(path, "rb") as f:
        f.seek(metadata["header_end"])  # pular o cabeçalho

        while True:
            chunk = f.read(1024)
            if not chunk:
                break

            # converte chunk em bits
            bits = "".join(f"{byte:08b}" for byte in chunk)

            # junta com bits pendentes
            bits = remaining_bits + bits

            # decodifica
            decoded, current_node, remaining_bits = decompress_stream(bits, current_node, tree)

            # junta o codigo decodigicado com o buffer anterior
            buffer += decoded

            # retorna a palavra se achar no buffer
            if word in buffer:
                return True

            # validação para não crescer infinitamente
            if len(buffer) > len(word) * 2:
                buffer = buffer[-len(word):]

    return False

def search_in_compressed_file_with_positions(path: str, word: bytes):
    tree, metadata = load_huffman_header(path)
    current_node = tree
    remaining_bits = ""

    word_len = len(word)

    buffer = b""    # para comparação de fronteira entre blocos/chunks
    positions = [] 

    # posição absoluta atual no texto descompactado
    absolute_pos = 0

    with open(path, "rb") as f:
        f.seek(metadata["header_end"])

        while True:
            chunk = f.read(1024)
            if not chunk:
                break

            # converte chunk em bits
            bits = "".join(f"{byte:08b}" for byte in chunk)
            bits = remaining_bits + bits

            decoded, current_node, remaining_bits = decompress_stream(bits, current_node, tree)

            if not decoded:
                continue

            window = buffer + decoded

            start = 0
            while True:
                index = window.find(word, start)
                if index == -1:
                    break

                # posição real = posição absoluta antes + índice relativo − buffer_extra
                real_pos = (absolute_pos - len(buffer)) + index
                if real_pos >= 0:
                    positions.append(real_pos)

                start = index + 1

            absolute_pos += len(decoded)

            # manter o buffer para pegar entre fontreiras
            if len(decoded) >= word_len:
                buffer = decoded[-word_len:]
            else:
                buffer = (buffer + decoded)[-word_len:]

    return positions
