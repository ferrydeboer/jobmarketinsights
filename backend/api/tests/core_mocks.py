import os
import sys
from unittest.mock import Mock

config_mock = Mock()
sys.modules["jomai.core.config"] = config_mock

settings_mock = Mock()
here = os.path.dirname(__file__)
# settings_mock.DATABASE_URI = f"sqlite:///{os.path.join(here, 'test.db')}"
# Could probably do this just as well with env files.
settings_mock.DATABASE_URI = f"sqlite://"
config_mock.settings = settings_mock

