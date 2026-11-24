class UnauthorizedError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UsernameAlreadyExistsError(Exception):
    pass


class NoPermissionError(Exception):
    pass


class UnknownUserCreateError(Exception):
    pass


class ProductAlreadyExistsError(Exception):
    pass


class UnknownProductCreateError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class NonExistentPageError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class CartItemNotFoundError(Exception):
    pass


class OrderNotFoundError(Exception):
    pass


class OrderAlreadyCancelledError(Exception):
    pass


class OrderCantBeCancelledError(Exception):
    pass


class CartIsEmptyError(Exception):
    pass


class PermissibleQuantityExceededError(Exception):
    pass


class InvalidOrderStatusTransitionError(Exception):
    pass