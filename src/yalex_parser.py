import re

class YALexParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.let_definitions = {}  # Definiciones de "let nombre = expr"
        self.rules = []  # Reglas de la sección "rule tokens ="

    def parse(self):
        """
        Devuelve un diccionario de tokens con sus expresiones regulares.
        """
        lines = self._read_file()
        self._parse_lets(lines)
        self._parse_rules(lines)
        tokens_dict = {}
        for rule_regex, rule_action in self.rules:
            expanded_regex = self._expand_macros(rule_regex)
            cleaned_regex = self.clean_regex(expanded_regex)
            if rule_action is not None:
                tokens_dict[rule_action] = cleaned_regex
            else:
                tokens_dict["WS"] = cleaned_regex
        return tokens_dict

    def _read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return f.readlines()

    def _parse_lets(self, lines):
        let_pattern = re.compile(r'^let\s+(\w+)\s*=\s*(.+)$')
        for line in lines:
            line = line.strip()
            if not line or line.startswith("(*"):
                continue
            m = let_pattern.match(line)
            if m:
                token_name = m.group(1).strip()
                regex = m.group(2).strip()
                cleaned = self.clean_regex(regex)
                self.let_definitions[token_name] = cleaned

    def _parse_rules(self, lines):
        in_rule_section = False
        for line in lines:
            line = line.strip()
            if line.startswith("rule tokens"):
                in_rule_section = True
                continue
            if in_rule_section:
                if not line:
                    continue
                line = re.sub(r'\(\*.*', '', line).strip()  # Eliminar comentarios "(* ... *)"
                if not line:
                    continue
                if line.startswith("|"):
                    line = line[1:].strip()
                if not line:
                    continue
                pattern = r"^(.+?)(?:\s*\{.*?return\s+(\w+).*?\})?$"
                match = re.match(pattern, line)
                if match:
                    rule_regex = match.group(1).strip()
                    action_token = match.group(2)
                    self.rules.append((rule_regex, action_token))

    def _expand_macros(self, rule_regex):
        rule_regex = rule_regex.strip()
        if rule_regex in self.let_definitions:
            return self._expand_macros(self.let_definitions[rule_regex])
        changed = True
        while changed:
            changed = False
            for name, definition in self.let_definitions.items():
                pattern = r'\b' + re.escape(name) + r'\b'
                new_rule_regex = re.sub(pattern, definition, rule_regex)
                if new_rule_regex != rule_regex:
                    rule_regex = new_rule_regex
                    changed = True
        return rule_regex

    def clean_regex(self, regex):
        """
        Limpia la expresión regular proveniente del .yal:
        - Para clases de caracteres (comienzan con '['), se procesa hasta el primer ']' encontrado,
          eliminando comillas simples y reemplazando saltos de línea y tabulaciones por sus secuencias.
        - Para literales (encerrados en comillas simples), se quitan las comillas y se escapa el literal.
        """
        regex = regex.strip()
        if regex.startswith("["):
            end = regex.find("]")
            if end != -1:
                inner = regex[1:end]
                inner = inner.replace("'", "")
                inner = inner.replace("\n", "\\n").replace("\t", "\\t")
                return "[" + inner + "]" + regex[end+1:]
        if (regex.startswith("''") and regex.endswith("''")) or (regex.startswith("'") and regex.endswith("'")):
            literal = regex.strip("'")
            return re.escape(literal)
        return regex
