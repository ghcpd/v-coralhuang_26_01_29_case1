"""Stub parser module"""

class Parser:
    """Base parser class"""
    
    FUNCTIONS = {}
    FUNCTION_PARSERS = {}
    FUNC_TOKENS = set()
    COLUMN_OPERATORS = {}
    TIMESTAMPS = set()
    RANGE_PARSERS = {}
    ALTER_PARSERS = {}
    IDENTIFY_PIVOT_STRINGS = False
    
    def __init__(self, tokens=None):
        self.tokens = tokens or []
    
    def parse(self):
        """Parse tokens into AST"""
        # Simplified: just return a string representation
        non_space_tokens = [t for t in self.tokens if t.text.strip()]
        return " ".join(t.text for t in non_space_tokens if t.text)


def binary_range_parser(cls):
    """Stub for binary range parser"""
    return lambda self: cls()
