from json import dumps

from django.test import TestCase

from perestroika.utils import dict_to_multi_dict


class DjangoTest(TestCase):
    def make_post(self, url, data):
        return self.client.post(url, dumps(data), content_type='application/json')

    def make_get(self, url, data):
        return self.client.get(url, dict_to_multi_dict(data), content_type='application/json')

    def test_allowed_methods(self):
        _response = self.make_post("/test/empty/", {})
        assert _response.status_code == 405

    def test_json_validation_no_items(self):
        _response = self.make_post("/test/full/", {"no": "data"})
        assert _response.status_code == 400

    def test_json_validation_wrong_order_type(self):
        _response = self.make_get("/test/full/",  {"order": "some order"})
        assert _response.status_code == 400

    def test_json_validation_wrong_order_item(self):
        _response = self.make_get("/test/full/", {"order": ["-1"]})
        assert _response.status_code == 400
