from pathlib import Path

_n = '\n'
_t = '\t'

def join_paths(*paths: Path):
	return SOURCE_FOLDER.joinpath(*paths)

SOURCE_FOLDER = Path(__file__).parent.parent.absolute()
