from setuptools import setup, find_packages

setup(
    name='sfs-helper',
    version='1.0',
    packages=find_packages(exclude=["test*", "venv"]),
    author='zk',
    author_email='dlzk@qq.com',
    url='http://www.sf-soft.com',
    description='Help SFSOFT Programmer Easy Python'
)
