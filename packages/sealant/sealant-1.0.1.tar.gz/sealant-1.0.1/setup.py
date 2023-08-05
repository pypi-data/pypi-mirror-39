from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='sealant',
    version='1.0.1',
    packages=['sealant'],
    url='https://pypi.org/project/sealant',
    license='LICENSE.md',
    author='ae.udahin',
    author_email='',
    description='Библиотека с инструментом для поиска утечек памяти в процессе выполнения тестов в Chrome или Node.js',
    install_requires=[
        'pychrome >= 0.2.2',
        'requests >= 2.19.1',
        'selenium >= 3.13.0'
    ]
)
