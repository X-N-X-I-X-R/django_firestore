class InsufficientFundsError(Exception):
    """Raised when user doesn't have enough funds for a transaction"""
    pass

class InvalidStatusError(Exception):
    """Raised when trying to perform an action on an object with invalid status"""
    pass

class InvalidAmountError(Exception):
    """Raised when amount is invalid (negative or zero)"""
    pass

class InvalidUserError(Exception):
    """Raised when user is not authorized to perform an action"""
    pass

class DuplicateTransactionError(Exception):
    """Raised when trying to create a duplicate transaction"""
    pass

class InvalidCoinError(Exception):
    """Raised when coin is invalid or already used"""
    pass

class PaymentProcessingError(Exception):
    """Raised when payment processing fails"""
    pass

class RefundProcessingError(Exception):
    """Raised when refund processing fails"""
    pass

class WithdrawalProcessingError(Exception):
    """Raised when withdrawal processing fails"""
    pass

class DepositProcessingError(Exception):
    """Raised when deposit processing fails"""
    pass

class TransferProcessingError(Exception):
    """Raised when transfer processing fails"""
    pass 