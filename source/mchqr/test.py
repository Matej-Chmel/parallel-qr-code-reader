from argparse import ArgumentParser
from inspect import signature
from mchqr.dev import PathList
from mchqr.io import dataset_paths, image_paths
from pathlib import Path
from typing import Callable, Union

PathAndPathListToNone = Callable[[Path, PathList], None]
PathListToNone = Callable[[PathList], None]

def test(function):
	tests[function.__name__] = function
	return function

tests = {}

@test
def all_tests():
	from mchqr.dev import _n

	for name, function in tests.items():
		if name == all_tests.__name__:
			continue

		print(f'{_n}Running test: {name}{_n}')
		function()

@test
def base_algorithm():
	from mchqr.algo import BaseAlgorithm
	from mchqr.dev import NotOverriden
	from mchqr.solution import AlgoSolution

	class BadAlgorithm(BaseAlgorithm):
		pass

	class GoodAlgorithm(BaseAlgorithm):
		def run(_) -> AlgoSolution:
			return 'Implemented.'

	def print_test(*algorithm_types):
		print(
			*map(
				lambda algorithm_type: test_algorithm(
					algorithm_type(None, None)
				),
				algorithm_types
			),
			sep='\n'
		)

	def test_algorithm(algo: BaseAlgorithm):
		try:
			return algo.measure()

		except NotOverriden as e:
			return e

	print_test(BadAlgorithm, GoodAlgorithm)

@test
def create_solution():
	from mchqr.algo import Sequence
	from mchqr.solution import dump_solution_to_file

	def save_decoded(path: Path, image_paths: PathList):
		elapsed, solution = run_zbar(Sequence, image_paths)

		dump_solution_to_file(
			path.joinpath('solution.json'),
			solution
		)
		print(
			format_elapsed(elapsed)
		)

	on_first_dataset(save_decoded)

def format_elapsed(elapsed: int):
	return f'Elapsed: {elapsed / 1_000_000_000 : .2f} seconds'

@test
def geometry():
	from mchqr.geometry import Size

	size = Size(100, 200)
	width, height = size

	print(
		size,
		size.as_tuple,
		[width, height],
		size.center,
		Size(4.1, 5.5).as_int,
		sep='\n'
	)

@test
def get_screen_size():
	from mchqr.platform import screen_size

	screen = screen_size()
	print(screen, screen.center, sep='\n')

ImageTest = Union[PathAndPathListToNone, PathListToNone]

@test
def list_image_paths():
	from mchqr.dev import _n, _t
	from mchqr.io import DATA_FOLDER, solution_path

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

def on_first_dataset(function: ImageTest):
	try:
		dataset = dataset_paths()[0]
		images = image_paths(dataset)

		if not images:
			return print("First dataset doesn't contain any images.")

		if len(
			signature(function).parameters
		) == 1:
			function(images)
		else:
			function(dataset, images)

	except IndexError:
		print('No dataset available.')

@test
def os():
	from mchqr.platform import OS

	print(OS)

@test
def process_pool():
	from mchqr.algo import ProcessPool

	print_first_dataset_solution_by_zbar(ProcessPool)

def print_first_dataset_solution_by_zbar(algo_type: type):
	from mchqr.solution import dump_solution_to_str

	def print_solution(image_paths: PathList):
		elapsed, solution = run_zbar(algo_type, image_paths)

		print(
			format_elapsed(elapsed),
			dump_solution_to_str(solution),
			sep='\n'
		)

	on_first_dataset(print_solution)

def run_zbar(algo_type: type, image_paths: PathList):
	from mchqr.detector import zbar
	from mchqr.image_list import ImageList

	return algo_type(
		zbar, ImageList.from_paths(image_paths)
	).measure()

@test
def sequence():
	from mchqr.algo import Sequence

	print_first_dataset_solution_by_zbar(Sequence)

@test
def show_image():
	from mchqr.image import Image
	from mchqr.platform import screen_size

	def show_first_image(image_paths: PathList):
		Image.from_path(
			image_paths[0]
		).resize_max(
			*screen_size()
		).show()

	on_first_dataset(show_first_image)

@test
def stroke_qr_codes():
	from mchqr.algo import Sequence
	from mchqr.detector import zbar
	from mchqr.geometry import Style
	from mchqr.image_list import ImageList

	def show_all(image_paths: PathList):
		images = ImageList.from_paths(image_paths)
		images.stroke(
			Sequence(zbar, images).run(),
			Style.dark_blue
		).show()

	on_first_dataset(show_all)

@test
def test_static_property():
	from dataclasses import dataclass
	from mchqr.dev import static_property

	@dataclass
	class Example:
		attribute: int

		@static_property
		def one():
			return Example(1)

	assert Example.one == Example(1)
	print('Both instances are equal.')

if __name__ == '__main__':
	parser = ArgumentParser(
		allow_abbrev=True,
		description='Runs visual testing of parallel QR code scanner.'
	)
	parser.add_argument(
		'test',
		default=None,
		help='Runs a test specified by its name.'
	)

	test = parser.parse_args().test.lower().replace(' ', '_')

	if test in tests:
		tests[test]()
	else:
		print(f"Test {test} doesn't exist.")
