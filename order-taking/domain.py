from typing import NewType, Union, NamedTuple, Tuple, List, Any, Callable, TypeVar, Generic
# this module is the place order workflow

# PlaceOrder is a function type
PlaceOrder = Callable[['UnvalidatedOrder'], 'PlaceOrderEvents']

PlaceOrderEvents = Union['AcknowledgementSent', 'OrderPlaced', 'BillableOrderPlaced']
AcknowledgementSent = Any
OrderPlaced = Any
BillableOrderPlaced = Any

ValidateOrder = Callable[['UnvalidatedOrder'], Union['ValidatedOrder', 'ValidationError']]

ValidatedOrder = NewType("ValidatedOrder", 'UnvalidatedOrder')
ValidationError = NamedTuple('ValidationError', [('field_name', str), ('description', str)])

GenericType = TypeVar('GenericType')


class NonEmptyList(Generic[GenericType]):
    def __init__(self, x: List[GenericType]):
        if not x:
            raise BaseException("List cannot be empty")
        self.value = x


class UnvalidatedOrder:
    def __init__(self, info: 'CustomerInfo', order_lines: NonEmptyList['OrderLine']):
        self.info = info
        self.order_lines = order_lines




OrderLine = Tuple['OrderQuantity', 'ProductCode']
CustomerInfo = NamedTuple('CustomerInfo', [('name', str), ('address', Any)])

# algebra of typesystems is something we all can benefit for having more
# what is a type?
UnitQuantity = NewType('UnitQuantity', int)
KilogramQuantity = NewType('KilogramQuantity', int)
OrderQuantity = Union[UnitQuantity, KilogramQuantity]


class ProductCode:
    def __init__(self, code: str):
        if code[0] != "W":
            raise BaseException("All product codes start with W")

        self._code = code


# tuples are good when there's no meaning added to the list composition

# end of model - just using the code above
my_order = UnvalidatedOrder(CustomerInfo(name="foo", address=None),
                            NonEmptyList([(UnitQuantity(6), ProductCode('Wabc'))]))

# look at the call stack start annotating the functions that are most used
# the right approach between an unccess type and an exception is semantical, also the rate of errors is important
# if is inherent in the design that things can fail you should treat as a separate type otherwise, is if some obscure edge
# case you should treat as an exception
