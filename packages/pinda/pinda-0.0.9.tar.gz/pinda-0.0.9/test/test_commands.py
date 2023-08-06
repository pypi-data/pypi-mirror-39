import pytest
from pinda import commands

def test_docker_available():
    result = commands.docker_installed()
    assert result is True
    result = commands.dicker_installed()
    assert result is False

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
    commands.install('vina', '1.1.2')
    with pytest.raises(ValueError):
        commands.install('vona', '1.1.2')

def test_uninstall():
    commands.uninstall('vina', '1.1.2')
    commands.uninstall('vina', '1.1.2')
    commands.uninstall('vona', '1.1.2')
