from pathlib import Path

_n = '\n'
_t = '\t'

def join_paths(*paths: Path):
	return SOURCE_FOLDER.joinpath(*paths)

def fopen(path: Path, mode='r', encoding='utf-8'):
	return open(path, mode, encoding=encoding)

SOURCE_FOLDER = Path(__file__).parent.parent.absolute()
