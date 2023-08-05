from abc import abstractmethod, ABC


class NonStringIterable(ABC):
    """Allow isinstance and issubclass to distinguish other iterable types from strings.

    isinstance("hello", NonStringIterable) -> False
    isinstance({"hello", "world"}, NonStringIterable) -> True
    """

    @abstractmethod
    def __iter__(self):
        while False:
            yield None

    @classmethod
    def __subclasshook__(cls, C):
        if cls is NonStringIterable:
            if issubclass(C, str):
                return False
            if any("__iter__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented
