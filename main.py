# main.py
from relations import parse_input
from normalizer import normalize
from printer import print_tables

def main(input_file, target_nf):
    relation = parse_input(input_file)
    
    # Normalize relations based on target NF
    normalize(relation, target_nf)
    
    print_tables(relation)

if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    target_nf = float(sys.argv[2])  # Highest NF (e.g., 3 for 3NF, 5 for 5NF)
    main(input_file, target_nf)
