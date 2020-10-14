import os
import sys
from unittest.mock import Mock

config_mock = Mock()
sys.modules["jomai.core.config"] = config_mock

settings_mock = Mock()
here = os.path.dirname(__file__)
#settings_mock.DATABASE_URI = f"sqlite:///{os.path.join(here, 'test.db')}"
settings_mock.DATABASE_URI = f"sqlite://"
config_mock.settings = settings_mock

# Need an improved version that keeps the in memory sessions open during
# the whole test.
# settings_mock.DATABASE_URI = f"sqlite://"
# config_mock.settings = settings_mock
#
# from jomai.db.session import get_session
# from alembic.config import Config
# from alembic import command
#
#
# cfgfile = os.path.join(here, "../jomai/alembic.ini")
# alembic_cfg = Config(cfgfile)
# os.chdir(os.path.join(here, "../jomai"))
#
# session: Session = next(get_session())
# command.upgrade(alembic_cfg, "head")
#
# os.chdir(here)
