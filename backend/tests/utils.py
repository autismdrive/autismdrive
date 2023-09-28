import uuid


def get_new_uuid():
    """returns a new uuid"""
    return str(uuid.uuid4())


class MockGoogleMapsClient:
    def geocode(self, address):
        return [{"geometry": {"location": {"lat": 0, "lng": 0}}}]
