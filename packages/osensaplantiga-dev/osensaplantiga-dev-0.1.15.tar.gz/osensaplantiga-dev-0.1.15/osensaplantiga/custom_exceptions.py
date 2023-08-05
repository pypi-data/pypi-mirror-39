class NoStructsFoundError(Exception):
    def __init__(self, message, errors):
        """Error to throw when trying to make structs but no structs can be created from bytes"""
        super(NoStructsFoundError, self).__init__(message)
