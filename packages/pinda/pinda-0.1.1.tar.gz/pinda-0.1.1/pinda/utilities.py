"""
utilities.py: pinda utility functions
"""
import subprocess
import os

from .data import database
def available_packages(name=None, version=None):
    result = []
    for record in database:
        if record['name'] == name or name is None:
            if str(record['version']) == str(version) or version is None:
                result.append(record)
    return result

def is_available(name, version):
    return len(available_packages(name, version)) == 1

def installed_packages(name=None, version=None):
    available = available_packages(name, version)
    if len(available) == 0:
        return []
    installed = []
    DEVNULL = open(os.devnull, 'w')
    listing = subprocess.check_output('pip list', universal_newlines=True, shell=True, stderr=DEVNULL).split('\n')
    for line in listing:
        words = line.split()
        if len(words) == 2:
            package = words[0]
            version = words[1]
            for p in available:
                if p['package'] == package and p['version'] == version:
                    installed.append(p)
    return installed

def is_installed(name, version):
    return len(installed_packages(name, version)) == 1

def docker_installed():
    try:
        result = subprocess.check_output('which docker', shell=True, 
                                          universal_newlines=True, 
                                          stderr=subprocess.STDOUT)
        return True
    except:
        return False
