from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse


class Serializer:
    pass


class DjangoSerializer:
    @staticmethod
    def get_encoder():
        return DjangoJSONEncoder

    def serialize(self, request, bundle):
        _data = {
            "limit": bundle.get("limit", 0),
            "skip": bundle.get("skip", 0),
            "total_count": bundle.get("total_count", 0),
        }

        if bundle.get("project"):
            _new_items = []

            for item in bundle["items"]:
                _new_item = {}

                for key in bundle["project"]:
                    _new_item[key] = item[key]

                _new_items.append(_new_item)

            bundle["items"] = _new_items

        _data['error_code'] = bundle.get('error_code', 0)

        _items = bundle.get("items", [])

        if len(_items) is 1:
            _data["item"] = _items[0]
        else:
            _data["items"] = _items

        if bundle.get("filter"):
            _data["filter"] = bundle["filter"]

        if bundle.get("order"):
            _data["order"] = bundle["order"]

        if bundle.get("project"):
            _data["project"] = bundle["project"]

        if bundle.get("profile_version"):
            _data["profile_version"] = bundle["profile_version"]

        return JsonResponse(_data, status=bundle['status_code'], encoder=self.get_encoder())
