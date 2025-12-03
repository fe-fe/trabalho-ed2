from file_utils import *
from huffman import build_huffman_frequency_tree, get_stream_byte_frequency, get_codes
import json


if __name__ == "__main__":
    freq_dict = dict()
    for c in get_binary_file_stream("test.txt"):
        get_stream_byte_frequency(c, freq_dict)
    tree = build_huffman_frequency_tree(freq_dict)
    code_list = list()
    get_codes(tree, code_list, str())
    print(code_list)