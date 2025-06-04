import re

class AFNtoAFD:
    def __init__(self, afn_list):
        """
        afn_list es un diccionario:
          { 'TOKEN_NAME': {'regex': '...'}, ... }
        """
        self.afn_list = afn_list

    def generate_python_code(self):
        token_patterns_code = []
        for token_name, afn_info in self.afn_list.items():
            regex = afn_info['regex']
            print(f"[DEBUG] Token={token_name}, Regex final='{regex}'")
            # Convertir la cadena a su representación de escape (para saltos de línea, tabulaciones, etc.)
            safe_regex = regex.encode('unicode_escape').decode('utf-8')
            # Si es un literal encerrado entre comillas simples, quitarlas y volver a escapar el contenido
            if safe_regex.startswith("\\'") and safe_regex.endswith("\\'"):
                literal = safe_regex[2:-2]
                safe_regex = re.escape(literal)
            token_patterns_code.append(f"    '{token_name}': r'{safe_regex}',")

        code = f'''import re

class Lexer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.token_patterns = {{
{chr(10).join(token_patterns_code)}
        }}

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
'''
        return code
