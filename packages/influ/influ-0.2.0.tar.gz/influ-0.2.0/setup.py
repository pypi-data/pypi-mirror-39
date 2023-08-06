from os import path

from setuptools import setup, find_packages


def long_description():
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        README = f.read()

    with open(path.join(here, 'HISTORY.md'), encoding='utf-8') as f:
        HISTORY = f.read()

    return '\n# ——————\n'.join([README, HISTORY])


setup(
    name='influ',
    version='0.2.0',
    description='Who influences whom in social network - an application for finding key nodes',
    long_description_content_type="text/markdown",
    long_description=long_description(),
    license='MIT',
    packages=find_packages(exclude=['test*']),
    author='Grzegorz Chilczuk',
    author_email='chgrzegorz@pm.me',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='graph social network influence',
    url='https://gitlab.com/chgrzegorz/dyplom-code',
    install_requires=[
        'python-igraph>=0.7.1.post6,<1.0.0',
        'numpy>=1.15.2,<2.0.0',
        'pandas>=0.23.4,<1.0.0',
        'PyYAML>=3.13.0,<4.0.0',
        'requests>=2.20.1,<3.0.0',
        'matplotlib>=3.0.0,<4.0.0',
        'pycairo>=1.17.1,<2.0.0',
    ],
    package_data={
        'influ': ['reader/datasets.yaml'],
    }
)
