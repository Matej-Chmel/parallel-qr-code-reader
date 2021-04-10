import cv2 as cv

def is_escape(key):
	return key == 27

def wait_key():
	return cv.waitKey(0)
