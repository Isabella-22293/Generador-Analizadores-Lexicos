import sys
import os
from src.yalex_parser import YALexParser
from src.regex_to_afn import RegexToAFN
from src.afn_to_afd import AFNtoAFD
from src.visualizer import Visualizer

def generate_lexer(yalex_file, output_file):
    parser = YALexParser(yalex_file)
    tokens = parser.parse()  # Diccionario: { "TOKEN_NAME": "regex" }

    afn_converter = RegexToAFN()
    afn_list = {}
    for token, expr in tokens.items():
        converted = afn_converter.convert(expr)
        afn_list[token] = {'regex': converted}

    afd_converter = AFNtoAFD(afn_list)
    lexer_code = afd_converter.generate_python_code()

    visualizer = Visualizer()
    visualizer.graph_afd(afd_converter, output_file.replace('.py', '_graph.txt'))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(lexer_code)

    print(f"Analizador léxico generado en {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[2] != "-o":
        print("Uso: python lexer_generator.py <archivo.yal> -o <output.py>")
        sys.exit(1)

    yalex_file = sys.argv[1]
    output_file = sys.argv[3]

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    generate_lexer(yalex_file, output_file)
