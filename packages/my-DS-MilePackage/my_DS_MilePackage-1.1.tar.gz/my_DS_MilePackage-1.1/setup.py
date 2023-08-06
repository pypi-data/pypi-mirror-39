from setuptools import setup, find_packages

setup(
    name='my_DS_MilePackage',
    version='1.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A test python package',
	url='https://github.com/khalad-hasan/myMileConverter',
    author='Dragon Warrior',
    author_email='debsarkar.00@gmail.com'
)
