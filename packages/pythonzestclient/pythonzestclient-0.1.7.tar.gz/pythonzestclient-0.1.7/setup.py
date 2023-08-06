__author__ = "Poonam Yadav"
__copyright__ = "Copyright 2007, The Databox Project"
__credits__ = ["Databox team"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Poonam Yadav"
__email__ = "p.yadav@acm.org"
__status__ = "Development"

from distutils.core import setup

setup(
  name = 'pythonzestclient',
  packages = ['pythonzestclient','pythonzestclient.exception'],
  version = '0.1.7',
  description = 'Python Client to connect to zest server',
  author = 'Poonam Yadav',
  author_email = 'poonam.hiwal@gmail.com',
  url = 'https://github.com/me-box/PythonZestClient',
  download_url = 'https://github.com/me-box/pythonzestclient/archive/0.1.7.tar.gz', # I'll explain this in a second
  keywords = ['zest client', 'databox project', 'datastore'],
  classifiers = [],
)