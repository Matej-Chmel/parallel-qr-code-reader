from . import tests as _tests
from .framework import test_arguments, tests
from mchqr.dev import StrList, to_str
from mchqr.io import fopen, SOURCE_FOLDER
from json import dump, load
from pathlib import Path

def all_test_configs() -> StrList:
	configs = []

	for test_name in tests:
		spaced_name = test_name.replace('_', ' ')

		if test_name in test_arguments:
			for args in test_arguments[test_name]:
				configs.append(
					', '.join([
						spaced_name, *map(to_str, args)
					])
				)
		else:
			configs.append(spaced_name)

	configs.sort()
	return configs

test_configs = all_test_configs()

def refresh_tests(json_path: Path):
	with fopen(json_path, 'r+') as file:
		config = load(file)
		inputs = config['inputs']
		test_input = next(
			input_entry for input_entry in inputs if input_entry['id'] == 'test'
		)
		test_input['options'] = test_configs

		file.seek(0)
		dump(config, file, indent=4)
		file.write('\n')

VSCODE_FOLDER = SOURCE_FOLDER.parent.joinpath('.vscode').absolute()

def vscode_json_path(filename: str) -> Path:
	return VSCODE_FOLDER.joinpath(f'{filename}.json')

if __name__ == '__main__':
	def vscode_refresh_tests(*filenames: str):
		for filename in filenames:	
			refresh_tests(
				vscode_json_path(filename)
			)

	vscode_refresh_tests('launch', 'tasks')
