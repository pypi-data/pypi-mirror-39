
SETUP_INFO = dict(
    name = 'infi.dnssimple',
    version = '0.0.7',
    author = 'Itai Shirav',
    author_email = 'itais@infinidat.com',

    url = 'https://git.infinidat.com/host-opensource/infi.dnssimple',
    license = 'PSF',
    description = """dnssimple utils""",
    long_description = """dnssimple utils""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'docopt',
'infi.traceback',
'requests[security]',
'setuptools'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [
'ddns = infi.dnssimple.scripts.ddns:main'
],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

