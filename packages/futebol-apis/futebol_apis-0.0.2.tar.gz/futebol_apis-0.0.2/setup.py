from setuptools import setup, find_packages

setup(
    name='futebol_apis',
    version='0.0.2',
    description='Schemas for the FUTEBOL services',
    url='http://github.com/nerds-ufes/futebol-apis',
    author='nerds',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=['protobuf'],
)
