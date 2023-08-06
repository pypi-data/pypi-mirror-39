import json
import re

from perestroika.exceptions import BadRequest
from perestroika.utils import multi_dict_to_dict

format_message = 'Right format: {' \
                 '"item(s)": ({} / []), ' \
                 '"filter": {"some": "value"}, ' \
                 '"order": ["-some", "index", "-with", "sign"]' \
                 '}'

class Deserializer:
    def deserialize(self, request, method):
        raise NotImplementedError()


class DjangoDeserializer(Deserializer):
    @staticmethod
    def need_objects(data):
        _has_items = "items" in data
        _has_item = "item" in data

        _has_any = _has_items or _has_item

        return not _has_any

    def deserialize(self, request, method):
        if request.method == 'GET':
            _data = multi_dict_to_dict(request.GET)
        else:
            _data = json.loads(request.body)

        format_error = self.need_objects(_data)

        # allow only django-orm order-by `-field/field`
        for item in _data.get("order", []):
            _match = re.match(r"(-[a-z_]*|[a-z_]*)", item)

            if not _match:
                format_error = True

            if len(_match.groups()) is not 1:
                format_error = True

            if _match.groups()[0] != item:
                format_error = True

        if format_error:
            raise BadRequest(message=format_message)

        _items = _data.get("items", [])
        _item = _data.get("item")

        if _item:
            _items = [_item]

        bundle = {
            "items": _items,
            "limit": 20,
            "skip": 0,
            "total_count": 0,
            "queryset": method.queryset,
            "project": _data.get("project", []),
        }

        if _data.get("filter"):
            bundle["filter"] = _data["filter"]

        if _data.get("order"):
            bundle["order"] = _data["order"]

        return bundle
