from mchqr.typing import DecodedList, StrFrozenSet

def extract_content(decoded_list: DecodedList) -> StrFrozenSet:
	return frozenset(
		map(
			lambda decoded: decoded.data.decode('utf-8'),
			decoded_list
		)
	)
