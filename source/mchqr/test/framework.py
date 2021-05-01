from argparse import ArgumentParser
from inspect import isclass, signature
from itertools import product
from mchqr.algo import algos, BaseAlgorithm
from mchqr.detector import detectors
from mchqr.dev import _n, AnyOrStrList, PathList, StrList, to_str
from mchqr.image import ImageList
from mchqr.io import dataset_paths, image_paths
from pathlib import Path
from typing import Callable, Iterable, Union

PathAndPathListToNone = Callable[[Path, PathList], None]
PathListToNone = Callable[[PathList], None]
TestNoArguments = Callable[[], None]
TestWithArguments = Callable[[StrList], None]

ArgumentCombinations = Iterable[StrList]
ImageTest = Union[PathAndPathListToNone, PathListToNone]
Test = Union[TestNoArguments, TestWithArguments]

def accepts_one_argument(function: Callable):
	return len(
		signature(function).parameters
	) == 1

def algo(arguments: AnyOrStrList, images: ImageList, test_name: str) -> BaseAlgorithm:
	if isclass(arguments[0]) and issubclass(arguments[0], BaseAlgorithm) and callable(arguments[1]):
		return arguments[0](
			arguments[1], images
		)

	try:
		return algos[arguments[0]](
			detectors[arguments[1]], images
		)

	except IndexError:
		return print(f'Test {test_name} accepts at least two arguments.')

ALGO_COMBINATIONS: ArgumentCombinations = tuple(
	product(algos.values(), detectors.values())
)

def main():
	parser = ArgumentParser(
		allow_abbrev=True,
		description='Runs visual testing of parallel QR code scanner.'
	)
	parser.add_argument(
		'test',
		default=None,
		help='Runs a test specified by its name.'
	)

	test, *arguments = parser.parse_args().test.split(',')
	test = test.lower().replace(' ', '_')

	if arguments:
		arguments = list(
			map(str.strip, arguments)
		)

	try:
		function = tests[test]

	except KeyError:
		return print(f"Test {test} doesn't exist.")

	if accepts_one_argument(function):
		function(arguments)
	else:
		function()

def on_first_dataset(function: ImageTest):
	try:
		dataset = dataset_paths()[0]

	except IndexError:
		print('No dataset available.')

	images = image_paths(dataset)

	if not images:
		return print("First dataset doesn't contain any images.")

	if accepts_one_argument(function):
		function(images)
	else:
		function(dataset, images)

def test(argument_combinations: ArgumentCombinations = None):
	def wrapped(function: Test):
		tests[function.__name__] = function

		if argument_combinations:
			test_arguments[function.__name__] = argument_combinations

		return function
	return wrapped

test_arguments = {}
tests = {}

@test()
def all_tests():
	def print_info(combination: ArgumentCombinations = None):
		text = f" with {', '.join(map(to_str, combination))}" if combination else ''
		print(f'{_n}Running test: {name}{text}{_n}')

	for name, function in tests.items():
		if name == all_tests.__name__:
			continue

		if name in test_arguments:
			for combination in test_arguments[name]:
				print_info(combination)
				function(combination)
		else:
			print_info()
			function()
