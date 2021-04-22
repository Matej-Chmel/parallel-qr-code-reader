from inspect import signature
from mchqr.data import dataset_paths, image_paths
from mchqr.typing import PathList
from pathlib import Path
from typing import Callable, Union

PathAndPathListToNone = Callable[[Path, PathList], None]
PathListToNone = Callable[[PathList], None]
TestFunction = Union[PathAndPathListToNone, PathListToNone]

def on_first_dataset(function: TestFunction):
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
