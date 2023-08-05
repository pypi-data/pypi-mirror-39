from setuptools import setup, find_packages
import re

VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
VERSIONFILE = "pinda/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RunTimeError("Unable to find version string in {}.".format(VERSIONFILE))

setup(
    name = 'pinda',
    version = verstr,
    packages = find_packages(),
    scripts = [
        'scripts/pinda',
    ],
)
