import sys
import os
from src.lexer_generator import generate_lexer

def main():
    if len(sys.argv) < 4 or sys.argv[2] != "-o":
        print("Uso: python main.py <archivo.yal> -o <output.py>")
        sys.exit(1)
    
    yalex_file = sys.argv[1]
    output_file = sys.argv[3]
    
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generate_lexer(yalex_file, output_file)

if __name__ == "__main__":
    main()
