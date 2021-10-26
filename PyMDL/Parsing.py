import json
from typing import Union
from .Infopage import InfoPage


def toJSON(data: Union[list, InfoPage], file: str = None):
    if type(data) == InfoPage:
        if file:
            with open(f'{file}.json', 'w') as f:
                json.dump(data.for_json(), f, indent=4)
        return json.loads(json.dumps(data.for_json(), indent=4))
    elif type(data) == list:
        all_items = {}
        for item in data:
            all_items = {**all_items, **item.for_json()}
        if file:
            file = file.rstrip('.json')
            with open(f'{file}.json', 'w') as f:
                json.dump(all_items, f, indent=4)
        return all_items.keys()
