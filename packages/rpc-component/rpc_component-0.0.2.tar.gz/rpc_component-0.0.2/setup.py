from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 2) and "install" in str(sys.argv):
    sys.exit('rpc-component requires Python >= 3.2 '
             'but the running Python is %s.%s.%s' % sys.version_info[:3])

setup(
    name='rpc_component',
    version='0.0.2',
    description='Tools for managing RPC components.',
    python_requires='>=3.2',
    install_requires=['GitPython', 'PyYAML', 'schema'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'component=rpc_component.cli:main',
        ],
    },
)
