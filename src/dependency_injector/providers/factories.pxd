"""Dependency injector factory providers.

Powered by Cython.
"""

from .base cimport Provider
from .callables cimport (
    Callable,
    __call as __call_callable,
)
from .injections cimport __inject_attributes


cdef class Factory(Provider):
    cdef Callable __instantiator

    cdef tuple __attributes
    cdef int __attributes_len

    cpdef object _provide(self, tuple args, dict kwargs)


cdef class DelegatedFactory(Factory):
    pass


cdef inline object __call(Factory self, tuple args, dict kwargs):
    cdef object instance

    instance = __call_callable(self.__instantiator, args, kwargs)

    if self.__attributes_len > 0:
        __inject_attributes(instance,
                            self.__attributes,
                            self.__attributes_len)

    return instance

