from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

BUY: Action
DESCRIPTOR: _descriptor.FileDescriptor
SELL: Action

class FollowerUpdateRequest(_message.Message):
    __slots__ = ["quantity", "stock_name", "transaction_number", "type"]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    quantity: int
    stock_name: str
    transaction_number: int
    type: Action
    def __init__(self, stock_name: _Optional[str] = ..., quantity: _Optional[int] = ..., type: _Optional[_Union[Action, str]] = ..., transaction_number: _Optional[int] = ...) -> None: ...

class FollowerUpdateResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class GetOrderRequest(_message.Message):
    __slots__ = ["order_number"]
    ORDER_NUMBER_FIELD_NUMBER: _ClassVar[int]
    order_number: int
    def __init__(self, order_number: _Optional[int] = ...) -> None: ...

class GetOrderResponse(_message.Message):
    __slots__ = ["name", "order_number", "quantity", "type"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORDER_NUMBER_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    order_number: int
    quantity: int
    type: Action
    def __init__(self, order_number: _Optional[int] = ..., name: _Optional[str] = ..., type: _Optional[_Union[Action, str]] = ..., quantity: _Optional[int] = ...) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class LookupRequest(_message.Message):
    __slots__ = ["stock_name"]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    stock_name: str
    def __init__(self, stock_name: _Optional[str] = ...) -> None: ...

class LookupResponse(_message.Message):
    __slots__ = ["max_volume", "price", "quantity", "volume"]
    MAX_VOLUME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    max_volume: int
    price: float
    quantity: int
    volume: int
    def __init__(self, price: _Optional[float] = ..., quantity: _Optional[int] = ..., volume: _Optional[int] = ..., max_volume: _Optional[int] = ...) -> None: ...

class OrderLogRecoverRequest(_message.Message):
    __slots__ = ["transaction_number"]
    TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    transaction_number: int
    def __init__(self, transaction_number: _Optional[int] = ...) -> None: ...

class OrderLogRecoverResponse(_message.Message):
    __slots__ = ["entries"]
    class OrderLogRecoverEntry(_message.Message):
        __slots__ = ["quantity", "stock_name", "transaction_number", "type"]
        QUANTITY_FIELD_NUMBER: _ClassVar[int]
        STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
        TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        quantity: int
        stock_name: str
        transaction_number: int
        type: Action
        def __init__(self, transaction_number: _Optional[int] = ..., stock_name: _Optional[str] = ..., type: _Optional[_Union[Action, str]] = ..., quantity: _Optional[int] = ...) -> None: ...
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[OrderLogRecoverResponse.OrderLogRecoverEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[OrderLogRecoverResponse.OrderLogRecoverEntry, _Mapping]]] = ...) -> None: ...

class OrderRequest(_message.Message):
    __slots__ = ["quantity", "stock_name", "type"]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    quantity: int
    stock_name: str
    type: Action
    def __init__(self, stock_name: _Optional[str] = ..., quantity: _Optional[int] = ..., type: _Optional[_Union[Action, str]] = ...) -> None: ...

class OrderResponse(_message.Message):
    __slots__ = ["transaction_number"]
    TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    transaction_number: int
    def __init__(self, transaction_number: _Optional[int] = ...) -> None: ...

class SignalOrderLeaderRequest(_message.Message):
    __slots__ = ["leader_port"]
    LEADER_PORT_FIELD_NUMBER: _ClassVar[int]
    leader_port: int
    def __init__(self, leader_port: _Optional[int] = ...) -> None: ...

class SignalOrderLeaderResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["action", "quantity", "stock_name"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    action: Action
    quantity: int
    stock_name: str
    def __init__(self, stock_name: _Optional[str] = ..., quantity: _Optional[int] = ..., action: _Optional[_Union[Action, str]] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    def __init__(self, status: _Optional[int] = ...) -> None: ...

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
