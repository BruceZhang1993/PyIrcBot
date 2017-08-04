from distutils.core import setup

setup(
    name='PyIrcBot',
    version='1.99',
    packages=['plugins', 'pyircbot'],
    url='https://github.com/BruceZhang1993/PyIrcBot',
    license='MIT',
    author='BruceZhang1993',
    author_email='zttt183525594@gmail.com',
    description='Yet another python based IRC bot framework.',
    scripts=['ircbot'],
    install_requires=[
        'irc',
        'termcolor',
        'requests',
        'Pillow',
        'BeautifulSoup4',
        'html5lib'
    ],
    keywords=['irc', 'bot']
)
