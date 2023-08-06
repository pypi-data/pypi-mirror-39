#User defined exceptions for gnfetcher
class NotFound(Exception):
    """Raised when the list articles in the function scapefeed() is empty"""
    pass
