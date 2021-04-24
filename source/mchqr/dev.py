from __future__ import annotations
from pathlib import Path
from typing import Callable, List, Union

_n = '\n'
_t = '\t'

class MessageException(Exception):
	def __init__(_, message: str = ''):
		super().__init__(message)

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
