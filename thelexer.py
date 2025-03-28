import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.token_patterns = {
    'delim': r'[' ''\t''\n']',
    'ws': r'delim+',
    'letter': r'['A'-'Z''a'-'z']',
    'digit': r'['0'-'9']',
    'id': r'letter(letter|digit)*',
        }
        
    def get_token(self):
        if self.position >= len(self.text):
            return ('EOF', None)

        # Buscamos la coincidencia más larga con alguno de los patrones
        longest_match = None
        matched_token_type = None

        for token_type, pattern in self.token_patterns.items():
            match = re.match(pattern, self.text[self.position:])
            if match:
                lexeme = match.group(0)
                # Verificar si es la coincidencia más larga
                if longest_match is None or len(lexeme) > len(longest_match):
                    longest_match = lexeme
                    matched_token_type = token_type

        if longest_match:
            self.position += len(longest_match)
            return (matched_token_type, longest_match)
        else:
            # No hay coincidencia => error léxico
            error_char = self.text[self.position]
            self.position += 1
            return ('ERROR', error_char)

if __name__ == "__main__":
    text = input("Ingrese el texto a analizar: ")
    lexer = Lexer(text)
    token = lexer.get_token()
    while token[0] != 'EOF':
        print("Token:", token)
        token = lexer.get_token()