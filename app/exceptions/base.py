# Not Found Errors
class NotFoundError(Exception):
    pass


class OrderNotFoundError(NotFoundError):
    pass


class CartItemNotFoundError(NotFoundError):
    pass


class ProductNotFoundError(NotFoundError):
    pass


class NonExistentPageError(NotFoundError):
    pass


# Already Exists Errors
class AlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(AlreadyExistsError):
    pass


class UsernameAlreadyExistsError(AlreadyExistsError):
    pass


class ProductAlreadyExistsError(AlreadyExistsError):
    pass


class CartIsEmptyError(AlreadyExistsError):
    pass


class UnauthorizedError(Exception):
    pass


class NoPermissionError(Exception):
    pass


class UnknownUserCreateError(Exception):
    pass


class UnknownProductCreateError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class ProductAlreadyArchivedError(Exception):
    pass


class ProductNotInArchiveError(Exception):
    pass


class PageSizeMustBeGreaterThanZeroError(Exception):
    pass


class OrderAlreadyCancelledError(Exception):
    pass


class OrderCantBeCancelledError(Exception):
    pass


class PermissibleQuantityExceededError(Exception):
    pass


class InvalidOrderStatusTransitionError(Exception):
    pass
