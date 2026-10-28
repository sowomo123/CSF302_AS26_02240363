import heapq
import os

# ============== HUFFMAN CODING ==============

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    """
    Build Huffman tree from character frequencies
    frequencies: dict {char: frequency}
    Returns: root of Huffman tree
    """
    # Create leaf nodes
    heap = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, HuffmanNode(char=char, freq=freq))
    
    # Build tree by combining nodes
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heap[0] if heap else None

def build_code_table(root, code="", code_table=None):
    """
    Build code table from Huffman tree
    code_table: dict {char: binary_code}
    """
    if code_table is None:
        code_table = {}
    
    if root is None:
        return code_table
    
    if root.char is not None:
        code_table[root.char] = code
        return code_table
    
    build_code_table(root.left, code + "0", code_table)
    build_code_table(root.right, code + "1", code_table)
    
    return code_table

def encode_text(text, code_table):
    """
    Encode text using Huffman code table
    Returns: bit string
    """
    encoded = ""
    for char in text:
        encoded += code_table[char]
    return encoded

def decode_text(encoded, root):
    """
    Decode bit string using Huffman tree
    Returns: original text
    """
    if root is None:
        return ""
    
    decoded = ""
    current = root
    
    for bit in encoded:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        
        if current.char is not None:
            decoded += current.char
            current = root
    
    return decoded

def get_frequencies(text):
    """
    Get character frequencies from text
    """
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies

def calculate_compression_ratio(text, encoded):
    """
    Calculate compression ratio compared to 8-bit fixed-length encoding
    """
    original_bits = len(text) * 8
    compressed_bits = len(encoded)
    ratio = original_bits / compressed_bits
    return ratio

# ============== DEMONSTRATION ==============
def demonstrate_huffman(filename):
    """
    Demonstrate Huffman coding on a text file
    """
    print("=" * 80)
    print(f"Huffman Coding: {filename}")
    print("=" * 80)
    print()
    
    # Read file
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"File length: {len(text)} characters")
    print(f"Original size (8-bit): {len(text) * 8} bits")
    print()
    
    # Get frequencies
    frequencies = get_frequencies(text)
    print(f"Unique characters: {len(frequencies)}")
    print()
    
    # Build Huffman tree
    root = build_huffman_tree(frequencies)
    
    # Build code table
    code_table = build_code_table(root)
    
    # Print code table
    print("Code Table:")
    print("-" * 80)
    for char in sorted(code_table.keys()):
        display_char = repr(char)[1:-1] if char != ' ' else 'space'
        print(f"  '{display_char}': {code_table[char]}")
    print()
    
    # Encode
    encoded = encode_text(text, code_table)
    print(f"Encoded length: {len(encoded)} bits")
    print()
    
    # Decode
    decoded = decode_text(encoded, root)
    
    # Verify
    print(f"Decoded length: {len(decoded)} characters")
    print(f"Verification: {'PASS' if decoded == text else 'FAIL'}")
    print()
    
    # Compression ratio
    ratio = calculate_compression_ratio(text, encoded)
    print(f"Compression ratio: {ratio:.2f}x")
    print(f"Space saved: {(1 - 1/ratio) * 100:.2f}%")
    print("=" * 80)
    print()
    
    return ratio

def create_test_files():
    """
    Create test text files for demonstration
    """
    # File 1: Simple text
    with open('test1.txt', 'w', encoding='utf-8') as f:
        f.write("hello world this is a test of huffman coding")
    
    # File 2: Repeated characters
    with open('test2.txt', 'w', encoding='utf-8') as f:
        f.write("aaaaabbbbbcccccdddddeeeeefffffggggghhhhh")
    
    # File 3: Mixed content
    with open('test3.txt', 'w', encoding='utf-8') as f:
        f.write("The quick brown fox jumps over the lazy dog. " * 10)

# ============== MAIN FUNCTION ==============
def main():
    create_test_files()
    
    # Test on three different files
    ratios = []
    for i in range(1, 4):
        ratio = demonstrate_huffman(f'test{i}.txt')
        ratios.append(ratio)
    
    print("=" * 80)
    print("Summary of Compression Ratios")
    print("=" * 80)
    for i, ratio in enumerate(ratios, 1):
        print(f"Test file {i}: {ratio:.2f}x compression")
    print(f"Average: {sum(ratios)/len(ratios):.2f}x compression")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
