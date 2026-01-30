"""Stub helper module"""


def seq_get(seq, index):
    """Get element from sequence at index, return None if out of bounds"""
    try:
        return seq[index]
    except (IndexError, KeyError):
        return None
