from json import dumps

from django.test import TestCase

from perestroika.utils import dict_to_multi_dict


class DjangoTest(TestCase):
    def make_post(self, url, data):
        return self.client.post(url, dumps(data), content_type='application/json')

    def make_empty_post(self, url):
        return self.client.post(url, content_type='application/json')

    def make_get(self, url, data):
        return self.client.get(url, dict_to_multi_dict(data), content_type='application/json')

    def test_allowed_methods(self):
        _response = self.make_post("/test/empty/", {})
        assert _response.status_code == 405

    def test_empty_get(self):
        _response = self.make_get("/test/full/", {})
        assert _response.status_code == 200

    def test_json_validation_no_items(self):
        _response = self.make_empty_post("/test/full/")
        assert _response.status_code == 400
        assert _response.json() == {
            'error_code': -1,
            'error_message': 'Need data for processing',
            'items': [],
            'limit': 0,
            'skip': 0,
            'status_code': 400,
            'total_count': 0
        }
