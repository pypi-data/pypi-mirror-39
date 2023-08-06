"""
data.py - the pinda database
"""
import os
import yaml
import pinda

default_database = [
            {
             'name': 'amber',
             'version': '16',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v16',
             'description': 'Amber and AmberTools version 16'
            },
            {
             'name': 'amber',
             'version': '18',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v18',
             'description': 'Amber and AmberTools version 18'
            },
            {
             'name': 'ambertools',
             'version': '16',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v16-tools',
             'description': 'AmberTools version 16'
            },
            {
             'name': 'ambertools',
             'version': '18',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v18-tools',
             'description': 'AmberTools version 18'
            },
            {
             'name': 'fpocket',
             'version': '3.0',
             'package': 'fpocketdocker',
             'repository': 'git+https://bitbucket.org/claughton/fpocket_docker.git',
             'description': 'FPocket version 3.0'
            },
            {
             'name': 'gromacs',
             'version': '2018',
             'package': 'gromacsdocker',
             'repository': 'git+https://bitbucket.org/claughton/gromacs_docker.git@v2018',
             'description': 'Gromacs version 2018'
            },
            {
             'name': 'gromacs',
             'package': 'gromacsdocker',
             'version': '2018-cuda',
             'repository': 'git+https://bitbucket.org/claughton/gromacs_docker.git@v2018-cuda',
             'description': 'Gromacs version 2018 with CUDA support'
            },
            {
             'name': 'obabel',
             'version': '2.4.1',
             'package': 'babeldocker',
             'repository': 'git+https://bitbucket.org/claughton/babel_docker.git',
             'description': 'Open Babel version 2.4.1',
            },
            {
             'name': 'vina',
             'version': '1.1.2',
             'package': 'vinadocker',
             'repository': 'git+https://bitbucket.org/claughton/vina_docker.git',
             'description': 'AutoDock Vina and selected AutoDock Tools',
            },
           ]

if not os.path.exists(pinda.PINDA_CONFIGDIR):
    os.mkdir(pinda.PINDA_CONFIGDIR)

if not os.path.exists(pinda.PINDA_CONFIGFILE):
    with open(pinda.PINDA_CONFIGFILE, 'w') as f:
        yaml.dump(default_database, f, default_flow_style=False)
    database = default_database
else:
    with open(pinda.PINDA_CONFIGFILE,'r') as f:
        database = yaml.load(f)
