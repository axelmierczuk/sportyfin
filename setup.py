from setuptools import setup

setup(
    name='sportyfin',
    version='0.1.0',
    author='Axel Mierczuk',
    author_email='axelmierczuk@gmail.com',
    packages=['sportyfin'],
    scripts=[],
    url='http://pypi.python.org/pypi/sportyfin/',
    license='LICENSE.txt',
    description='Scrapes popular streaming sites and compiles m3u/xml files for viewing.',
    long_description=open('README.md').read(),
    install_requires=[
        "async-generator==1.10",
        "attrs==21.4.0",
        "beautifulsoup4==4.10.0",
        "bs4==0.0.1",
        "certifi==2021.10.8",
        "cffi==1.15.0",
        "charset-normalizer==2.0.10",
        "chromedriver-binary==97.0.4692.71.0",
        "cryptography==36.0.1",
        "h11==0.12.0",
        "idna==3.3",
        "lxml==4.7.1"
        "outcome==1.1.0",
        "Pillow==9.0.0",
        "pycparser==2.21",
        "pyOpenSSL==21.0.0",
        "python-dotenv==0.19.2",
        "regex==2021.11.10",
        "requests==2.27.1",
        "selenium==4.1.0",
        "six==1.16.0",
        "sniffio==1.2.0",
        "sortedcontainers==2.4.0"
        "soupsieve==2.3.1",
        "trio==0.19.0",
        "trio-websocket==0.9.2",
        "urllib3==1.26.8",
        "wsproto==1.0.0"
    ],
)
