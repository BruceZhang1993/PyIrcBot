from distutils.core import setup
from setuptools import find_packages

setup(
    name='Py-IrcBot',
    version='0.2',
    packages=find_packages(),
    url='https://github.com/BruceZhang1993/PyIrcBot',
    license='GPL',
    author='BruceZhang1993',
    author_email='zttt183525594@gmail.com',
    description='A python3-based irc title bot.',
    entry_points={
        'console_scripts': [
            'ircbot=pyircbot.main:main'
        ]
    },
    install_requires=['irc', 'termcolor', 'requests', 'BeautifulSoup4', 'Pillow', 'html5lib'],
)
