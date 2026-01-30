"""
Minimal Token and Tokenizer implementation for testing
"""

from enum import auto
from typing import List, Union, Tuple


class TokenType:
    """Token type constants"""
    # Basic types
    VAR = auto()
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    AS = auto()
    JOIN = auto()
    LEFT = auto()
    RIGHT = auto()
    INNER = auto()
    OUTER = auto()
    ON = auto()
    USING = auto()
    GROUP = auto()
    BY = auto()
    HAVING = auto()
    ORDER = auto()
    LIMIT = auto()
    OFFSET = auto()
    UNION = auto()
    INTERSECT = auto()
    EXCEPT = auto()
    DISTINCT = auto()
    ALL = auto()
    TABLE = auto()
    CREATE = auto()
    DROP = auto()
    ALTER = auto()
    INSERT = auto()
    UPDATE = auto()
    DELETE = auto()
    TRUNCATE = auto()
    INTO = auto()
    VALUES = auto()
    SET = auto()
    
    # Data types
    INT = auto()
    VARCHAR = auto()
    CHAR = auto()
    TEXT = auto()
    BOOLEAN = auto()
    FLOAT = auto()
    DOUBLE = auto()
    DECIMAL = auto()
    DATE = auto()
    TIME = auto()
    TIMESTAMP = auto()
    TIMESTAMPTZ = auto()
    TIMESTAMPLTZ = auto()
    
    # Operators
    EQ = auto()
    NEQ = auto()
    GT = auto()
    GTE = auto()
    LT = auto()
    LTE = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    PIPE = auto()
    DPIPE = auto()
    ARROW = auto()
    DARROW = auto()
    HASH = auto()
    COLON = auto()
    DCOLON = auto()
    COMMA = auto()
    DOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    BACKSLASH = auto()
    AMP = auto()
    CARET = auto()
    TILDA = auto()
    
    # Special
    PARAMETER = auto()
    PLACEHOLDER = auto()
    COMMENT = auto()
    SPACE = auto()
    BREAK = auto()
    UNKNOWN = auto()
    EOF = auto()
    
    # Function-specific
    RLIKE = auto()
    
    # Snowflake-specific
    ILIKE_ANY = auto()
    LIKE_ANY = auto()
    MATCH_RECOGNIZE = auto()
    COMMAND = auto()
    REPLACE = auto()
    TABLE_SAMPLE = auto()


class Token:
    """Represents a token"""
    def __init__(self, token_type: TokenType, text: str, line: int = 1, col: int = 1):
        self.token_type = token_type
        self.text = text
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.token_type}, {self.text!r})"


class Tokenizer:
    """Base tokenizer class"""
    
    # Comment delimiters - can be single strings (line comment) or tuples (block comment)
    COMMENTS: List[Union[str, Tuple[str, str]]] = ["--", ("/*", "*/")]
    
    # Quotes for strings
    QUOTES = ["'", '"']
    
    # String escape characters
    STRING_ESCAPES = ["\\"]
    
    # Hex string delimiters
    HEX_STRINGS = []
    
    # Keywords mapping
    KEYWORDS = {}
    
    # Single character tokens
    SINGLE_TOKENS = {}
    
    # Variable single tokens
    VAR_SINGLE_TOKENS = set()
    
    def __init__(self):
        self.sql = ""
        self.size = 0
        self.tokens = []
        self._current = 0
        self._line = 1
        self._col = 1
    
    def tokenize(self, sql: str) -> List[Token]:
        """
        Tokenize SQL string.
        This is a simplified implementation that focuses on comment handling.
        """
        self.sql = sql
        self.size = len(sql)
        self._current = 0
        self._line = 1
        self._col = 1
        self.tokens = []
        
        while self._current < self.size:
            # Try to match comments
            if self._scan_comment():
                continue
            
            # Try to match whitespace
            if self._scan_whitespace():
                continue
            
            # Try to match keywords and identifiers
            if self._scan_keyword_or_identifier():
                continue
            
            # Try to match numbers
            if self._scan_number():
                continue
            
            # Try to match strings
            if self._scan_string():
                continue
            
            # Try to match operators and punctuation
            if self._scan_operator():
                continue
            
            # Unknown character - add as identifier for now
            char = self.sql[self._current]
            self.tokens.append(Token(TokenType.UNKNOWN, char, self._line, self._col))
            self._advance()
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, "", self._line, self._col))
        
        return self.tokens
    
    def _peek(self, offset: int = 0) -> str:
        """Peek at character at current + offset"""
        pos = self._current + offset
        if pos < self.size:
            return self.sql[pos]
        return ""
    
    def _advance(self, count: int = 1) -> str:
        """Advance current position"""
        chars = ""
        for _ in range(count):
            if self._current < self.size:
                char = self.sql[self._current]
                chars += char
                self._current += 1
                if char == '\n':
                    self._line += 1
                    self._col = 1
                else:
                    self._col += 1
        return chars
    
    def _scan_comment(self) -> bool:
        """Scan and skip comments"""
        for comment_delimiter in self.COMMENTS:
            if isinstance(comment_delimiter, tuple):
                # Block comment (start, end)
                start, end = comment_delimiter
                if self.sql[self._current:self._current + len(start)] == start:
                    # Find end of block comment
                    self._advance(len(start))
                    while self._current < self.size:
                        if self.sql[self._current:self._current + len(end)] == end:
                            self._advance(len(end))
                            break
                        self._advance()
                    return True
            else:
                # Line comment
                if self.sql[self._current:self._current + len(comment_delimiter)] == comment_delimiter:
                    # Skip until end of line
                    while self._current < self.size and self.sql[self._current] != '\n':
                        self._advance()
                    return True
        return False
    
    def _scan_whitespace(self) -> bool:
        """Scan whitespace"""
        if self._peek() in (' ', '\t', '\n', '\r'):
            start = self._current
            while self._peek() in (' ', '\t', '\n', '\r'):
                self._advance()
            # Add whitespace token
            text = self.sql[start:self._current]
            self.tokens.append(Token(TokenType.SPACE, text, self._line, self._col))
            return True
        return False
    
    def _scan_keyword_or_identifier(self) -> bool:
        """Scan keyword or identifier"""
        char = self._peek()
        if char.isalpha() or char == '_':
            start = self._current
            while self._peek().isalnum() or self._peek() == '_':
                self._advance()
            text = self.sql[start:self._current]
            
            # Check if it's a keyword
            token_type = self.KEYWORDS.get(text.upper(), TokenType.IDENTIFIER)
            self.tokens.append(Token(token_type, text, self._line, self._col))
            return True
        return False
    
    def _scan_number(self) -> bool:
        """Scan number"""
        if self._peek().isdigit():
            start = self._current
            while self._peek().isdigit() or self._peek() == '.':
                self._advance()
            text = self.sql[start:self._current]
            self.tokens.append(Token(TokenType.NUMBER, text, self._line, self._col))
            return True
        return False
    
    def _scan_string(self) -> bool:
        """Scan string literal"""
        char = self._peek()
        if char in self.QUOTES:
            quote = char
            self._advance()  # Opening quote
            start = self._current
            
            while self._current < self.size:
                if self.sql[self._current] == quote:
                    # Check if escaped
                    if self._current > 0 and self.sql[self._current - 1] in self.STRING_ESCAPES:
                        self._advance()
                        continue
                    # End of string
                    text = self.sql[start:self._current]
                    self._advance()  # Closing quote
                    self.tokens.append(Token(TokenType.STRING, text, self._line, self._col))
                    return True
                self._advance()
            
            # Unterminated string
            text = self.sql[start:self._current]
            self.tokens.append(Token(TokenType.STRING, text, self._line, self._col))
            return True
        return False
    
    def _scan_operator(self) -> bool:
        """Scan operators and punctuation"""
        char = self._peek()
        
        operators = {
            '=': TokenType.EQ,
            '>': TokenType.GT,
            '<': TokenType.LT,
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.STAR,
            '/': TokenType.SLASH,
            '%': TokenType.PERCENT,
            '|': TokenType.PIPE,
            '#': TokenType.HASH,
            ':': TokenType.COLON,
            ',': TokenType.COMMA,
            '.': TokenType.DOT,
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            '[': TokenType.LBRACKET,
            ']': TokenType.RBRACKET,
            '{': TokenType.LBRACE,
            '}': TokenType.RBRACE,
            ';': TokenType.SEMICOLON,
            '&': TokenType.AMP,
            '^': TokenType.CARET,
            '~': TokenType.TILDA,
        }
        
        if char in operators:
            self.tokens.append(Token(operators[char], char, self._line, self._col))
            self._advance()
            return True
        
        return False
