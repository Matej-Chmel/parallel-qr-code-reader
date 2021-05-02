import cv2 as cv
from mchqr.image import Image
from mchqr.solution import AlgoPair, Detected, DetectedList
import numpy as np
from pyzbar.pyzbar import decode, Decoded, ZBarSymbol
from typing import Callable, List

DecodedList = List[Decoded]
Detector = Callable[[Image], AlgoPair]

def algo_pair(image: Image, detected_list: DetectedList):
	return AlgoPair(image.name, detected_list)

def detector(function: Detector):
	detectors[function.__name__] = function
	return function

detectors = {}

@detector
def cv_detector(image: Image):
	_, data_list, bounding_boxes, _ = cv.QRCodeDetector().detectAndDecodeMulti(image.matrix)

	return algo_pair(
		image, [
			Detected(
				data_list[i],
				np.int32(
					bounding_boxes[i]
				)
			)
			for i in range(
				len(data_list)
			)
		]
	)

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
