class AdvException(Exception):
    """
    Base exception so that all Advocate SDK Exceptions can be caught be a single root exception if necessary
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class APIException(AdvException):
    """
    Exception for catching communication errors with the Advocate API
    """
    pass


class UpdateError(AdvException):
    """
    Called when an attempt to create or update an object (Widget, DCTA, etc) fails
    """
    pass


class RenderError(AdvException):
    """
    Called when a render fails
    """
    pass


class NoMatchException(AdvException):
    """
    Called when an particular item is requested from the server but it
    is not found or not in the user's valid items
    """
    def __init__(self, item_type, check_field, check_value):
        self.item_type = item_type
        self.check_field = check_field
        self.check_value = check_value
        self.message = (
            '{} with {} value "{}" either does not exist or cannot be accessed '
            'by this Advocate user.'. format(
                self.item_type,
                self.check_field,
                self.check_value,
            )
        )
