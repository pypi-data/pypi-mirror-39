from setuptools import setup, find_packages

setup(
    name='treatWithYoga',
    version='0.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A test python package',
	url='https://github.com/rroygithub/data-533-lab4-mohsen-roy',
    author='Rajeev Roy',
    author_email='rajeev.roy@gmail.com',
    install_requires=['csv','matplotlib']
)