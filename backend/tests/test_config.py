from tests.base_test import BaseTest  # isort:skip
from tests.utils import set_env_var


class TestConfig(BaseTest):
    def test_config(self):
        rv = self.client.get("/api/config", follow_redirects=True, content_type="application/json")
        self.assert_success(rv)
        response = rv.json
        self.assertEqual(response["mirroring"], False)
        self.assertEqual(response["testing"], True)
        self.assertEqual(response["development"], False)

    def test_config_load_local_settings(self):
        from config.base import Settings
        import os

        _settings0 = self.settings  # from BaseTest, where ENV_NAME is "testing"
        _settings1: Settings
        _settings2: Settings
        _settings3: Settings
        _settings4: Settings
        fail_diff_msg = "Should be different instances, because ENV_NAME has changed."
        fail_same_msg = "Should be the same instance, because ENV_NAME has not changed."

        with set_env_var("ENV_NAME", "local"):
            from config.load import SettingsSingleton

            assert os.environ["ENV_NAME"] == "local", f"ENV_NAME is {os.environ['ENV_NAME']} instead of 'local'"  # isort:skip

            # Ensure all subsequent instances are the same
            _settings1 = SettingsSingleton()
            _settings2 = SettingsSingleton()

            assert _settings1 is not _settings0, fail_diff_msg
            assert _settings1 is _settings2, fail_same_msg
            assert _settings1.ENV_NAME == "local", f"Expected ENV_NAME to be 'local', got '{_settings1.ENV_NAME}'"

        with set_env_var("ENV_NAME", "testing"):
            from config.load import SettingsSingleton

            assert os.environ["ENV_NAME"] == "testing", f"ENV_NAME is {os.environ['ENV_NAME']} instead of 'testing'"  # isort:skip

            # Ensure all subsequent instances are the same, but different from previous ones
            _settings3 = SettingsSingleton()
            _settings4 = SettingsSingleton()

            assert _settings3 is not _settings1, fail_diff_msg
            assert _settings3 is _settings4, fail_same_msg
            assert _settings3.ENV_NAME == "testing", f"Expected ENV_NAME to be 'testing', got '{_settings3.ENV_NAME}'"
