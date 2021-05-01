from .framework import algo, ALGO_COMBINATIONS, on_first_dataset, test
import cv2 as cv
from dataclasses import dataclass
from itertools import cycle
from mchqr.geometry import Color, Size, Style
from mchqr.algo import BaseAlgorithm, Sequence
from mchqr.detector import zbar
from mchqr.dev import _n, _t, AnyOrStrList, NotOverriden, PathList, static_property
from mchqr.image import Image, ImageList, ImageView
from mchqr.io import DATA_FOLDER, dataset_paths, image_paths, solution_path
from mchqr.platform import OS, screen_size
from mchqr.solution import AlgoSolution, dump_solution_to_file, dump_solution_to_str
import numpy as np
from pathlib import Path

@test()
def base_algorithm():
	class BadAlgorithm(BaseAlgorithm):
		pass

	class GoodAlgorithm(BaseAlgorithm):
		def run(_) -> AlgoSolution:
			return 'Implemented.'

	def print_test(*algorithm_types):
		print(
			*(
				test_algorithm(
					algorithm_type(None, None)
				)
				for algorithm_type in algorithm_types
			),
			sep='\n'
		)

	def test_algorithm(algo: BaseAlgorithm):
		try:
			return algo.measure()

		except NotOverriden as e:
			return e

	print_test(BadAlgorithm, GoodAlgorithm)

@test()
def color_splits():
	colors = cycle([
		Color.full_blue, Color.full_green, Color.full_red
	])
	split_size = Size(1024, 1024)

	def build(image: Image):
		build_matrix = np.zeros(image.shape, np.uint8)
		last_row_color = None
		y = -1

		for view in image.split(split_size):
			view: ImageView

			color = next(colors)

			if y != view.origin.y:
				if color == last_row_color:
					color = next(colors)

				last_row_color = color
				y = view.origin.y

			split = build_matrix[view.index()]
			split[:] = color

			cv.addWeighted(
				split, 0.3,
				view.matrix, 0.7, 0,
				split
			)

		return image.new(build_matrix)

	def show(image_paths: PathList):
		ImageList((
			build(image)
			for image in ImageList.from_paths(image_paths)
		)).show()

	on_first_dataset(show)

@test()
def create_solution():
	def save_decoded(path: Path, image_paths: PathList):
		elapsed, solution = Sequence(
			zbar, ImageList.from_paths(image_paths)
		).measure()

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

@test()
def geometry():
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

@test()
def get_screen_size():
	screen = screen_size()
	print(screen, screen.center, sep='\n')

@test()
def list_image_paths():
	def format_entry(path: Path):
		return f'{_t}{path.stem}'

	def solution_info(path: Path):
		try:
			text = solution_path(path).name
		
		except FileNotFoundError as e:
			text = e

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

@test()
def os():
	print(OS)

@test(ALGO_COMBINATIONS)
def measure(arguments: AnyOrStrList):
	def print_solution(image_paths: PathList):
		elapsed, solution = algo(
			arguments, ImageList.from_paths(image_paths), measure.__name__
		).measure()

		print(
			format_elapsed(elapsed),
			dump_solution_to_str(solution),
			sep='\n'
		)

	on_first_dataset(print_solution)

@test()
def show_image():
	def show_first_image(image_paths: PathList):
		Image.from_path(
			image_paths[0]
		).resize_max(
			*screen_size()
		).show()

	on_first_dataset(show_first_image)

@test(ALGO_COMBINATIONS)
def stroke_qr_codes(arguments: AnyOrStrList):
	def show_all(image_paths: PathList):
		images = ImageList.from_paths(image_paths)
		images.stroke(
			algo(arguments, images, stroke_qr_codes.__name__).run(),
			Style.dark_blue
		).show()

	on_first_dataset(show_all)

@test()
def test_static_property():
	@dataclass
	class Example:
		attribute: int

		@static_property
		def one():
			return Example(1)

	assert Example.one == Example(1)
	print('Both instances are equal.')
