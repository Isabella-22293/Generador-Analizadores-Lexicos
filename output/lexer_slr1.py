import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.token_patterns = {
            'WS': r'[ \t\n]+',  # Corregido el patrón para WS
            'ID': r'[A-Za-z]([A-Za-z]|[0-9])*',  # Corregido el patrón para ID
            'NUMBER': r'\d+(\.\d+)?([eE][+-]?\d+)?',  # Corregido el patrón para números (incluye notación científica)
            'PLUS': r'\+',  # Corregido el patrón para PLUS
            'TIMES': r'\*',  # Corregido el patrón para TIMES
            'LPAREN': r'\(',  # Corregido el patrón para LPAREN
            'RPAREN': r'\)',  # Corregido el patrón para RPAREN
        }

    def get_token(self):
        while self.position < len(self.text):
            longest_match = None
            matched_token_type = None

            for token_type, pattern in self.token_patterns.items():
                match = re.match(pattern, self.text[self.position:])
                if match:
                    lexeme = match.group(0)
                    if longest_match is None or len(lexeme) > len(longest_match):
                        longest_match = lexeme
                        matched_token_type = token_type

            if longest_match:
                self.position += len(longest_match)
                # Saltar espacios en blanco (token WS)
                if matched_token_type == 'WS':
                    continue
                return (matched_token_type, longest_match)
            else:
                error_char = self.text[self.position]
                self.position += 1
                return ('ERROR', error_char)
        return ('EOF', None)

if __name__ == "__main__":
    text = input("Ingrese el texto a analizar: ")
    lexer = Lexer(text)
    token = lexer.get_token()
    while token[0] != 'EOF':
        print("Token:", token)
        token = lexer.get_token()
