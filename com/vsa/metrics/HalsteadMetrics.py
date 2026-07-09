from com.vsa.elements import languages


class HalsteadMetrics:
    """Counts operator/operand token frequencies for a source file using the
    selected language's operator set. Returns [operators, operands] dicts that
    the CSV layer aligns to the language vocabulary."""

    def __init__(self, language='java'):
        self.language = languages.get(language)

    def get_features(self):
        """The token vocabulary used as CSV feature columns (language-specific)."""
        return self.language.vocabulary

    def run(self, programFileName):
        # Operators come from the selected language (not a static file), so the
        # metric respects the language. Longest tokens first so compound
        # operators ('<=', '==', '//') match before their single-char prefixes.
        operator_tokens = sorted(set(self.language.operators), key=len, reverse=True)
        operators = {token: 0 for token in self.language.operators}
        operands = {}

        isAllowed = True
        with open(programFileName) as f:
            for line in f:
                line = line.strip("\n").strip(' ')
                if line.startswith("/*"):
                    isAllowed = False
                if (not line.startswith("//")) and isAllowed and (not line.startswith('#')):
                    for key in operator_tokens:
                        operators[key] = operators[key] + line.count(key)
                        line = line.replace(key, ' ')
                    for key in line.split():
                        operands[key] = operands.get(key, 0) + 1
                if line.endswith("*/"):
                    isAllowed = True
        return [operators, operands]
