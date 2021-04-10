from pathlib import Path
from mchqr import _n, _t, join_paths

DATA_FOLDER = join_paths('data')

def yield_datasets():
	return (folder for folder in DATA_FOLDER.iterdir() if folder.is_dir())

def yield_image_files(path: Path):
	return (file for file in path.rglob('*') if file.is_file() and file.suffix.lower() in ['.jpg', '.png'])

if __name__ == '__main__':
	def format_entry(path: Path):
		return f'{_t}{path.stem}'

	datasets = list(yield_datasets())

	print(
		f'Path to data folder: {DATA_FOLDER}',
		'Available datasets:',
		*[format_entry(dataset) for dataset in datasets],
		'\n\n'.join(
			f'{dataset.stem}:{_n}{_n.join(format_entry(image) for image in yield_image_files(dataset))}'
			for dataset in datasets
		),
		sep='\n'
	)
