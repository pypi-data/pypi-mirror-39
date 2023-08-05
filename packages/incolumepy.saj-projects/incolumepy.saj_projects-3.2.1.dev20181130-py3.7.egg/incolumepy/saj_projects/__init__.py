# See http://peak.telecommunity.com/DevCenter/setuptools
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

import os
import logging.config
import yaml


conffile = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'logger.yml'))
assert os.path.isfile(conffile), f"{conffile} inexistente"

with open(conffile, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

with open(os.path.join(os.path.join(os.path.dirname(__file__), "version.txt"))) as f:
    __version__ = f.read().strip()

__package__ = 'incolumepy.saj_projects'


if __name__ == '__main__':
    print(f"package '{__package__}': Version '{__version__}'")
