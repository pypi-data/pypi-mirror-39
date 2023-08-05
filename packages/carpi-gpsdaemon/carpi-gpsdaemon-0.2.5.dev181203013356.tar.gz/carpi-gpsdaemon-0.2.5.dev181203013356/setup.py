"""
CARPI REDIS DATA BUS
(C) 2018, Raphael "rGunti" Guntersweiler
Licensed under MIT
"""
import os
from datetime import datetime
from time import time

from setuptools import setup


# ### READING DOCUMENTATION TO RST #########################
def convert_md_to_rst(file: str):
    with open(file, 'r') as f:
        return f.read()


# ### READING VERSION.txt NUMBER ###############################
def read_version():
    with open('VERSION.txt', 'r') as f:
        return f.read().strip()


def get_version():
    build_time = datetime.fromtimestamp(time())
    base_ver = read_version()

    if 'CI_BUILD_REF_NAME' in os.environ:
        branch = os.environ['CI_BUILD_REF_NAME']
        if branch == "develop":
            # Develop Build
            return '{}.dev{}'.format(base_ver,
                                     build_time.strftime('%y%m%d%H%M%S'))
        elif branch.startswith('release/'):
            # Release Candidate Build
            base_ver = branch.split('/')[1]
            return "{}rc{}".format(base_ver,
                                   build_time.strftime('%y%m%d%H%M%S'))
        else:
            # Release Build
            return os.environ['CI_BUILD_REF_NAME']
    else:
        return '{}.dev{}'.format(base_ver,
                                 build_time.strftime('%y%m%d%H%M%S'))


# ### PRINTING ENVIRONMENT VARIABLES #######################
# for key, val in os.environ.items():
#     print(" -- ENV {} = {}".format(key, val))

# ### DEFINING PROJECT PROPERTIES ##########################
NAME = "carpi-gpsdaemon"
VERSION = get_version()
DESCRIPTION = open('SHORT_DESCRIPTION.txt', 'r').read()
LONG_DESCRIPTION = convert_md_to_rst('README.md')

AUTHOR = "rGunti"
AUTHOR_EMAIL = "raphael@rgunti.ch"
LICENSE = "MIT"
URL = "https://gitlab.com/rGunti/CarPi-GPSDaemon"

PACKAGES = [
    'gpsdaemon'
]
DEPENDENCIES = [
    'wheel',
    'gps3',
    'carpi-daemoncommons',
    'carpi-redisdatabus'
]
OPTIONAL_DEPENDENCIES = {}
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6'
]

# ### BUILDING #############################################
print(" >> Building {} Ver. {}".format(NAME, VERSION))
setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=PACKAGES,
      install_requires=DEPENDENCIES,
      extras_require=OPTIONAL_DEPENDENCIES,
      classifiers=CLASSIFIERS,
      url=URL,
      zip_safe=False,
      include_packaged_data=True)
