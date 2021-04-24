import cv2 as cv
from mchqr import PathList, StrList
from pathlib import Path

def dataset_paths() -> PathList:
	return [folder for folder in DATA_FOLDER.iterdir() if folder.is_dir()]

def fopen(path: Path, mode='r', encoding='utf-8'):
	return open(path, mode, encoding=encoding)

def glob_by_extensions(path: Path, extensions: StrList) -> PathList:
	return [file for file in path.rglob('*') if file.is_file() and file.suffix.lower() in extensions]

def image_paths(path: Path):
	return glob_by_extensions(path, ['.jpg', '.png'])

def is_escape(key: int):
	return key == 27

def join_paths(*paths: Path):
	return SOURCE_FOLDER.joinpath(*paths)

def solution_path(path: Path):
	try:
		return glob_by_extensions(path, ['.json'])[0]
	
	except IndexError:
		raise FileNotFoundError(
			f"Dataset {path.stem} doesn't contain any solution file."
		)

def wait_key():
	return cv.waitKey(0)

SOURCE_FOLDER = Path(__file__).parent.parent.absolute()
DATA_FOLDER = join_paths('data')
