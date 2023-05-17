from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Response(_message.Message):
    __slots__ = ["ip", "process"]
    IP_FIELD_NUMBER: _ClassVar[int]
    PROCESS_FIELD_NUMBER: _ClassVar[int]
    ip: str
    process: int
    def __init__(self, ip: _Optional[str] = ..., process: _Optional[int] = ...) -> None: ...

class non(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
