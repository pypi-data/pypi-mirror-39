from setuptools import setup, find_packages

setup(
    name='MohsenPackage',
    version='0.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A test python package',
	url='https://github.com/khalad-hasan/myMileConverter',
    author='M Zardadi',
    author_email='zardadi@gmail.com'
)