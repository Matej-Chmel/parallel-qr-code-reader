from mchqr.image import Image
from pyzbar.pyzbar import decode, ZBarSymbol

def detect(image: Image):
	return decode(image.matrix, [ZBarSymbol.QRCODE])

if __name__ == '__main__':
	from json import dumps, JSONEncoder
	from mchqr.data import dataset_paths, image_paths

	class ZBarEncoder(JSONEncoder):
		def default(_, o):
			if isinstance(o, bytes):
				return o.decode('utf-8')

			return super().default(o)

	try:
		first_dataset = dataset_paths()[0]

		try:
			print(
				dumps(
					detect(
						Image(
							image_paths(first_dataset)[0]
						)
					),
					cls=ZBarEncoder,
					indent=4
				)
			)

		except IndexError:
			print('No images to show.')

	except IndexError:
		print('No available datasets.')
