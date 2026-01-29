"""
Mock sqlglot implementation for testing the Snowflake comment parsing fix.

This is a minimal implementation that includes just enough functionality to test
the comment parsing behavior. In a real scenario, this would be the actual sqlglot library.
"""

from snowflake import Snowflake


def parse_one(sql, read=None):
    """
    Parse a SQL string and return an AST.
    
    Args:
        sql: The SQL string to parse
        read: The dialect to use for parsing (e.g., 'snowflake', 'postgres')
    
    Returns:
        An AST representation of the query
    """
    # Map dialect names to dialect classes
    dialect_map = {
        'snowflake': Snowflake,
        'postgres': Snowflake,  # Using Snowflake for all for simplicity in this mock
        'mysql': Snowflake,
        'sqlite': Snowflake,
    }
    
    # Get the dialect class
    dialect_name = read.lower() if read else 'snowflake'
    dialect_class = dialect_map.get(dialect_name, Snowflake)
    
    # Create dialect instance
    dialect = dialect_class()
    
    # Tokenize
    tokenizer = dialect.Tokenizer()
    tokens = list(tokenizer.tokenize(sql))
    
    # Parse
    parser = dialect.Parser(tokens=tokens)
    ast = parser.parse()
    
    return ast
