"""Stub generator module"""

class Generator:
    """Base generator class"""
    
    TRANSFORMS = {}
    TYPE_MAPPING = {}
    PROPERTIES_LOCATION = {}
    
    PARAMETER_TOKEN = "?"
    MATCHED_BY_SOURCE = True
    SINGLE_STRING_INTERVAL = False
    JOIN_HINTS = True
    TABLE_HINTS = True
