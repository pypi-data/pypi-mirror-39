import re
import sys
from os.path import join, dirname
from setuptools import setup, find_packages

package_name = 'smsit'
py_version = sys.version_info[:2]

# reading package's version
with open(join(dirname(__file__), package_name, '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(
        v_file.read()
    ).group(1)

dependencies = [
    'requests'
]
if py_version < (3, 5):
    dependencies.append('typing')

setup(
    name=package_name,
    version=package_version,
    author='Mahdi Ghanea.g',
    description='A simple wrapper to send SMS through available gateways.',
    long_description=open('README.rst').read(),
    url='https://github.com/meyt/smsit',
    packages=find_packages(),
    install_requires=dependencies,
    license='MIT License',
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
