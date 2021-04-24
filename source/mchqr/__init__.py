from pathlib import Path
from pyzbar.pyzbar import Decoded
from typing import List, FrozenSet

_n = '\n'
_t = '\t'
DecodedList = List[Decoded]
DecodedMatrix = List[DecodedList]

class MessageException(Exception):
	def __init__(_, message: str = ''):
		super().__init__(message)

class NoScreen(MessageException):
	pass

class NotOverriden(MessageException):
	def __init__(_, method_name: str):
		super().__init__(
			f'Method {method_name} is abstract and must be overriden.'
		)

PathList = List[Path]

class static_property(property):
    def __get__(self, _, owner):
        return staticmethod(self.fget).__get__(None, owner)()

StrFrozenSet = FrozenSet[str]
StrList = List[str]
