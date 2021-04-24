from mchqr.image import Image
from mchqr.solution import AlgoPair, Detected
import numpy as np
from pyzbar.pyzbar import decode, Decoded, ZBarSymbol
from typing import Callable, List

DecodedList = List[Decoded]
Detector = Callable[[Image], AlgoPair]

def zbar(image: Image) -> AlgoPair:
	return AlgoPair(
		image.name, [
			Detected(
				decoded.data.decode('utf-8'),
				np.array(decoded.polygon)
			)
			for decoded in decode(image.matrix, [ZBarSymbol.QRCODE])
		]
	)
