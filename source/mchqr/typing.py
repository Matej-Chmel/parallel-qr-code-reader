from pathlib import Path
from pyzbar.pyzbar import Decoded
from typing import Dict, List, FrozenSet

DecodedList = List[Decoded]
DecodedMatrix = List[DecodedList]
PathList = List[Path]
StrFrozenSet = FrozenSet[str]
StrList = List[str]

Solution = Dict[str, StrFrozenSet]
