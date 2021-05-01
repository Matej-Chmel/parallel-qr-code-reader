from mchqr.image import Image
from mchqr.solution import AlgoPair, Detected, DetectedList
import numpy as np
from pyzbar.pyzbar import decode, Decoded, ZBarSymbol
from typing import Callable, List
from zxing import BarCodeReader

DecodedList = List[Decoded]
Detector = Callable[[Image], AlgoPair]

def algo_pair(image: Image, detected_list: DetectedList):
	return AlgoPair(image.name, detected_list)

def detector(function: Detector):
	detectors[function.__name__] = function
	return function

detectors = {}

@detector
def zbar(image: Image):
	return algo_pair(
		image, [
			Detected(
				decoded.data.decode('utf-8'),
				np.array(decoded.polygon)
			)
			for decoded in decode(
				image.matrix, [ZBarSymbol.QRCODE]
			)
		]
	)

@detector
def zxing(image: Image):
	barcodes = BarCodeReader().decode(
		image.path_as_str, possible_formats=["QR_CODE"]
	)

	if not isinstance(barcodes, list):
		barcodes = [barcodes]

	return algo_pair(
		image, [
			Detected(
				barcode.raw,
				np.array(barcode.points, dtype=np.int32)
			)
			for barcode in barcodes
		]
	)
