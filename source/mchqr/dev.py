from __future__ import annotations
from numpy import ndarray
from pathlib import Path
from typing import Any, Callable, List, Union

_n = '\n'
_t = '\t'

AnyList = List[Any]

class MessageException(Exception):
	def __init__(_, message: str = ''):
		super().__init__(message)

NdArrayList = List[ndarray]

class NoScreen(MessageException):
	pass

class NotOverriden(MessageException):
	def __init__(_, method: Overridable):
		name = (
			f'Property {method.fget.__qualname__}'
			if isinstance(method, property)
			else f'Method {method.__qualname__}'
		)
		super().__init__(
			f'{name} is abstract and must be overriden.'
		)

Overridable = Union[Callable, property]
PathList = List[Path]

class static_property(property):
    def __get__(self, _, owner):
        return staticmethod(self.fget).__get__(None, owner)()

StrList = List[str]

def subclasses(_class: type):
	return _class.__subclasses__()

def subclasses_dict(_class: type):
	return {
		_class.__name__: _class
		for _class in subclasses(_class)
	}

def to_str(object):
	if isinstance(object, str):
		return object

	return object.__name__

AnyOrStrList = Union[AnyList, StrList]
