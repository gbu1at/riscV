def to_int32(x):
    if isinstance(x, str):
        if x.startswith("0x"):
            x = int(x, 16)
        else:
            x = int(x)

    x %= 2 ** 32
    if x >= 2 ** 31:
        x = x - 2 ** 32
    return x


def get_last_N_bits(number, N):
    assert(N > 0)
    last_N_bits = to_int32(number) & ((1 << N) - 1)
    binary_string = bin(last_N_bits)[2:]
    padded_bits = binary_string.zfill(N)
    return padded_bits

def get_segment_bits(number:str, l, r):
    assert(r > l)
    seg_bits = ((to_int32(number) + 2 ** 33) & ((1 << r) - 1)) >> l
    binary_string = bin(seg_bits)[2:]
    padded_bits = binary_string.zfill(r - l)
    return padded_bits


def reverse(s):
    return "".join(reversed(s))


def binary_to_hex(binary_string):
    assert(len(binary_string) == 32)
    byte_array = reversed(bytearray(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8)))
    hex_string = ' '.join(f"{byte:02X}" for byte in byte_array)
    return hex_string


import re

def clean_text(text):
    lines = text.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]

    cleaned_lines = []
    for line in non_empty_lines:
        if cleaned_lines and cleaned_lines[-1].rstrip().endswith(','):
            cleaned_lines[-1] = cleaned_lines[-1].rstrip() + ' ' + line.strip()
        else:
            cleaned_lines.append(line.strip())


    final_text = '\n'.join(cleaned_lines)

    return final_text
