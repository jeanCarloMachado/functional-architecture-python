from typing import NewType, Union, NamedTuple, Tuple, List, Any, Callable, TypeVar, Generic
from functools import reduce, partial
from shared import Command, NonEmptyList

# this module is the place order workflow

OrderTakingCommand = Union['PlaceOrder', 'ChangeOrder', 'CancelOrder']
ChangeOrder = Command[Any]
CancelOrder = Command[Any]
PlaceOrder = Command['UnvalidatedOrder']

# PlaceOrder workflow - is a function type
PlaceOrderWorkFlow = Callable[[PlaceOrder], 'PlaceOrderEvents']
PlaceOrderEvents = Union['AcknowledgementSent', 'OrderPlaced', 'BillableOrderPlaced']

AcknowledgementSent = Any
OrderPlaced = Any
BillableOrderPlaced = Any

ValidationError = NamedTuple('ValidationError', [('field_name', str), ('description', str)])

OrderId = NewType('OrderId', str)

UnvalidatedOrder = NamedTuple('UnvalidatedOrder', [
    ('order_id', OrderId),
    ('customer_info', 'CustomerInfo'),
    ('billing_address', 'Address'),
    ('shipping_address', 'Address'),
    ('order_lines', NonEmptyList['OrderLine']),
])

ValidatedOrder = NamedTuple('ValidatedOrder', [
    ('order_id', OrderId),
    ('customer_info', 'CustomerInfo'),
    ('billing_address', 'Address'),
    ('shipping_address', 'Address'),
    ('order_lines', NonEmptyList['OrderLine']),
])

PricedOrder = NamedTuple('PricedOrder', [
    ('order_id', OrderId),
    ('customer_info', 'CustomerInfo'),
    ('billing_address', 'Address'),
    ('shipping_address', 'Address'),
    ('order_lines', NonEmptyList['OrderLine']),
    ('amount_to_bill', 'Price'),
])

Order = Union[UnvalidatedOrder, ValidatedOrder, PricedOrder]

# @property
# def price(self) -> 'Price':
#     return Price(reduce(lambda a, b: a + int(b[1]), self.order_lines.value, 0))

OrderLine = Tuple['OrderQuantity', 'Price', 'ProductCode']
CustomerInfo = NamedTuple('CustomerInfo', [('name', str)])
Address = NewType('Address', str)

Price = NewType('Price', float)

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


CheckProductExists = Callable[[ProductCode], bool]
CheckAddressExists = Callable[['UnvalidatedAddress'], 'ValidatedAddress']


def validate_order(check_product_exists: CheckProductExists, check_address_exists: CheckAddressExists, order: UnvalidatedOrder) -> Union['ValidatedOrder', 'ValidationError']:
    for order_line in order.order_lines.value:
        if not check_product_exists(order_line[2]):
            return ValidationError('order_line', 'order line is not valid')

    if not check_address_exists(order.billing_address):
        return ValidationError('billing_address', 'billing_address is not valid')

    if not check_address_exists(order.shipping_address):
        return ValidationError('billing_address', 'shipping_address is not valid')

    return ValidatedOrder(order.order_id, order.customer_info, order.billing_address, order.shipping_address, order.order_lines)

validate_order_injected = partial(validate_order, lambda x: True, lambda x: ValidatedAddress)

UnvalidatedAddress = Address
ValidatedAddress = NewType('ValidatedAddress', Address)

# tuples are good when there's no meaning added to the list composition

# end of model - just using the code above
my_order = UnvalidatedOrder(
    OrderId("666"), CustomerInfo(name="foo"), Address(''), Address(''),
    NonEmptyList([(UnitQuantity(6), Price(321), ProductCode('Wabc')),
                  (UnitQuantity(6), Price(123), ProductCode('Wabc'))]))

validated_order = validate_order_injected(my_order)
# look at the call stack start annotating the functions that are most used
# the right approach between an unccess type and an exception is semantical, also the rate of errors is important
# if is inherent in the design that things can fail you should treat as a separate type otherwise, is if some obscure edge
# case you should treat as an exception
