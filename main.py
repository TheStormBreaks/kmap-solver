import os
import itertools
import math

def get_user_input():
    """Get number of variables and minterms from the user."""
    num_vars = int(input("Enter the number of variables: "))
    max_entries = 2 ** num_vars

    print(f"Enter the minterms (integers from 0 to {max_entries - 1}):")
    minterms = list(map(int, input("Minterms: ").split()))
    
    if any(m < 0 or m >= max_entries for m in minterms):
        raise ValueError("Minterms must be within valid range.")

    return num_vars, minterms

def generate_kmap(num_vars, minterms):
    """Generate a k-map given the number of variables and minterms."""
    rows, cols = (2 ** (num_vars // 2), 2 ** (num_vars - num_vars // 2))
    kmap = [[0 for _ in range(cols)] for _ in range(rows)]

    for minterm in minterms:
        binary = f"{minterm:0{num_vars}b}"
        row = int(binary[:len(binary)//2], 2)
        col = int(binary[len(binary)//2:], 2)
        kmap[row][col] = 1

    return kmap

def print_kmap(kmap):
    """Pretty print the k-map."""
    for row in kmap:
        print(" ".join(map(str, row)))

def find_groups(kmap):
    rows, cols = len(kmap), len(kmap[0])
    groups = []

    for group_size in [8, 4, 2, 1]:
        for r in range(rows):
            for c in range(cols):
                if kmap[r][c] == 1:
                    group = [(r + dr, c + dc) for dr in range(group_size // cols) for dc in range(group_size % cols)]
                    if all(kmap[r % rows][c % cols] == 1 for r, c in group):
                        groups.append(group)
                        for r, c in group:
                            kmap[r][c] = -1
    return groups

def group_to_expressions(group, num_vars):
    literals = []
    for i in range(num_vars):
        bits = set((coord[i] for coord in group))
        if len(bits) == 1:
            literals.append(chr(65 + i) if bits.pop() == 1 else f"~{chr(65 + i)}")
    return " & ".join(literals)
        
def solve_kmap(num_vars, kmap):
    groups = find_groups(kmap)
    expressions = [group_to_expressions(group, num_vars) for group in groups]
    return " + ".join(expressions)

if __name__ == "__main__":
    # File: main.py
    num_vars, minterms = get_user_input()
    kmap = generate_kmap(num_vars, minterms)

    print("K-Map:")
    print_kmap(kmap)

    expression = solve_kmap(num_vars, kmap)
    print("Simplified Boolean Expression:", expression)
