from setuptools import setup

setup(
    name='bruce-ircbot',
    version='2.00',
    packages=['pyircbot', 'pyircbot.plugins'],
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
