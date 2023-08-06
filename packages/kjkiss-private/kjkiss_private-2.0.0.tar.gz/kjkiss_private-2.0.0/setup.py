from distutils.core import setup
import setuptools

with open('README') as file:
    readme = file.read()
    
setup(
    name='kjkiss_private',
    version = '2.0.0',
    packages=['wargame'],
    #url = 'https://testpypi.python.org/pypi/kjkiss_game/',
    url = 'http://192.168.1.10:8081/simple',
	license = 'LICENSE.txt',
    description='my private game',
    long_description=readme,
    author='kjkiss',
    author_email='kjkiss@163.com')	
    