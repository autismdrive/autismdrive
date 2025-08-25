import json


class MockRequestsResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def __iter__(self):
        if isinstance(self.json_data, list):
            for item in self.json_data:
                yield item
        elif isinstance(self.json_data, dict):
            for attr, value in self.json_data.items():
                yield attr, value
        else:
            yield self.json_data

    def json(self):
        return self.json_data

    @property
    def text(self):
        return json.dumps(self.json_data, default=str)


class MockResponse(MockRequestsResponse):
    @property
    def json(self):
        return self.json_data
