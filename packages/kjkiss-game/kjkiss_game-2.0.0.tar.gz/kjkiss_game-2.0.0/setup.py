from distutils.core import setup
import setuptools

with open('README') as file:
    readme = file.read()
    
setup(
    name='kjkiss_game',
    version = '2.0.0',
    packages=['wargame'],
    url = 'https://testpypi.python.org/pypi/kjkiss_game/',
    license = 'LICENSE.txt',
    description='my fantasy game',
    long_description=readme,
    author='kjkiss',
    author_email='kjkiss@163.com')	
    