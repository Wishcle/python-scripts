import json
from pathlib import Path
import pprint

import dacite

from amtrak.models.journey import JourneyResponse


class Processor:
    def __init__(self) -> None:
        self.response_file = Path("response.json")

    def process(self) -> None:
        self._load_file()
        self._load_model()

    def _load_file(self) -> None:
        assert self.response_file is not None
        assert self.response_file.exists()
        assert self.response_file.is_file()

        with open(self.response_file) as f:
            data = json.load(f)
            self.response_data = data

    def _load_model(self) -> None:
        assert self.response_data is not None

        def to_camel_case(key: str) -> str:
            first_part, *remaining_parts = key.split('_')
            return first_part + ''.join(part.title() for part in remaining_parts)

        response = dacite.from_dict(
            data_class=JourneyResponse,
            data=self.response_data,
            config=dacite.Config(convert_key=to_camel_case))

        pprint.pprint(response)
