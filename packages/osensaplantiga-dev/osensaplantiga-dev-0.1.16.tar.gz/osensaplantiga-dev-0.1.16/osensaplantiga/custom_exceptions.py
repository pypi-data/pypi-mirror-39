class NoStructsFoundError(Exception):
    """Error to throw when trying to make structs but no structs can be created from bytes"""


class NoBytesFoundError(Exception):
    """Error to throw when trying to create structs but no bytes are present"""
