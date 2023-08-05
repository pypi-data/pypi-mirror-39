import pytest
from pinda import commands

def test_available_all():
    result = commands.available_packages()
    assert type(result) == list

def test_available_specific():
    result = commands.available_packages('gromacs')
    assert len(result) == 2
    for r in result:
        assert r['name'] == 'gromacs'

def test_available_specific_version():
    result = commands.available_packages('gromacs', '2018')
    assert len(result) == 1
    for r in result:
        assert r['version'] == '2018'
    
def test_installed_packages():
    result = commands.installed_packages('gromacs', '2018')
    assert len(result) == 1
    result = commands.is_installed('gromacs', '2018')
    assert result == True
    result = commands.is_installed('gromacs', '2018-cuda')
    assert result == False

def test_install():
    result = commands.install('vina', '1.1.2')
    assert result == True

def test_uninstall():
    result = commands.uninstall('vina', '1.1.2')
    assert result == True
