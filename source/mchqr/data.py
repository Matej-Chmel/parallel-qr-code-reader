from mchqr import _n, _t, join_paths

from mchqr.typing import PathList, StrList
from pathlib import Path

DATA_FOLDER = join_paths('data')

def dataset_paths() -> PathList:
	return [folder for folder in DATA_FOLDER.iterdir() if folder.is_dir()]

def glob_by_extension(path: Path, extensions: StrList) -> PathList:
	return [file for file in path.rglob('*') if file.is_file() and file.suffix.lower() in extensions]

def image_paths(path: Path):
	return glob_by_extension(path, ['.jpg', '.png'])

def solution_path(path: Path):
	try:
		return glob_by_extension(path, ['.json'])[0]
	
	except IndexError:
		raise FileNotFoundError(
			f"Dataset {path.stem} doesn't contain any solution file."
		)

if __name__ == '__main__':
	def format_entry(path: Path):
		return f'{_t}{path.stem}'

	def solution_info(path: Path):
		try:
			text = solution_path(path).name
		
		except FileNotFoundError as e:
			text = str(e)
		
		return f'{_t}{text}'

	datasets = dataset_paths()

	print(
		f'Path to data folder: {DATA_FOLDER}',
		'Available datasets:',
		*[format_entry(dataset) for dataset in datasets],
		'\n\n'.join(
			f'{dataset.stem}:{_n}'
			f'{_n.join(format_entry(image) for image in image_paths(dataset))}{_n}'
			f'{solution_info(dataset)}'
			for dataset in datasets
		),
		sep='\n'
	)
