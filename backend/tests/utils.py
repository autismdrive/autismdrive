import os
import uuid
from contextlib import contextmanager

from tests.fixtures.fixture_utils import fake


@contextmanager
def set_env_var(var_name, value):
    # Save the original value
    original_value = os.environ.get(var_name)

    # Overwrite the environment variable
    os.environ[var_name] = value
    try:
        yield  # Yield control back to the test
    finally:
        # Restore the original value
        if original_value is not None:
            os.environ[var_name] = original_value
        else:
            del os.environ[var_name]  # Remove if it didn't exist


def get_new_uuid():
    """returns a new uuid"""
    return str(uuid.uuid4())


class MockGoogleMapsClient:
    def geocode(self, address: dict = None):
        lat, lng = 0, 0

        if address:
            # Use address hash value to create a seed for the fake lat/long
            # so that the same address always returns the same lat/long
            fake.seed_instance(hash(address))
            lat, lng = fake.latlng()

        return [{"geometry": {"location": {"lat": lat, "lng": lng}}}]


def ordinal(n: int):
    """
    Convert an integer into its ordinal representation.
    """
    suffix = "th" if (11 <= (n % 100) <= 13) else ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix
