from setuptools import setup

setup(
    name='spark-monitoring',
    version='0.0.1',
    packages=['examples', 'sparkmonitoring'],
    url='https://bliseng.github.io/spark-monitoring/',
    license='LGPL3',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    description='A python library to interact with the Spark History server',
    install_requires=['requests'],
    extras_requires={'pandas': ['pandas', 'matplotlib']},
    build_requires=['pydoc-markdown'],
)
