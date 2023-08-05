"""
commands.py: pinda commands
"""
import subprocess

from .data import database
def available_packages(name=None, version=None):
    result = []
    for record in database:
        if record['name'] == name or name is None:
            if record['version'] == version or version is None:
                result.append(record)
    return result

def is_available(name, version):
    return len(available_packages(name, version)) == 1

def installed_packages(name=None, version=None):
    available = available_packages(name, version)
    if len(available) == 0:
        return []
    installed = []
    listing = subprocess.check_output('pip list', universal_newlines=True, shell=True, stderr=subprocess.DEVNULL).split('\n')
    for line in listing:
        words = line[:-1].split()
        if len(words) == 2:
            package = words[0]
            version = words[1]
            for p in available:
                if p['package'] == package and p['version'] == version:
                    installed.append(p)
    return installed

def is_installed(name, version):
    return len(installed_packages(name, version)) == 1

def install(name, version, sudo=False, user=True):
    if is_installed(name, version):
        return True
    r = available_packages(name, version)[0]
    if sudo:
        command = 'sudo pip install {repository}'.format(**r)
    else:
        if user:
            command = 'pip install {repository} --user'.format(**r)
        else:
            command = 'pip install {repository}'.format(**r)
    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True, stderr = subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False
    
def uninstall(name, version, sudo=False):
    if not is_installed(name, version):
        return True
    r = available_packages(name, version)[0]
    if sudo:
        command = 'sudo pip uninstall -y{package}'.format(**r)
    else:
        command = 'pip uninstall -y {package}'.format(**r)
    try:
        result = subprocess.check_output(command, shell=True, universal_newlines=True, stderr = subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False
    
