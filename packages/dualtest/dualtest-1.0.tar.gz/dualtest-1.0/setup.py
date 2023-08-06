from pathlib import Path
from setuptools import setup


desc = 'Easily test both Python and C versions of modules.'
readme = Path('README.rst')

setup(
    name='dualtest',
    version='1.0',
    description=desc,
    long_description=readme.read_text(),

    py_modules=['dualtest'],
    test_suite='tests',
    )
