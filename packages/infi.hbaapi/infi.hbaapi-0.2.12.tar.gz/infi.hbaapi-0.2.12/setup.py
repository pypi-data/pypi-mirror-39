
SETUP_INFO = dict(
    name = 'infi.hbaapi',
    version = '0.2.12',
    author = 'Arnon Yaari',
    author_email = 'arnony@infinidat.com',

    url = 'https://github.com/Infinidat/infi.hbaapi',
    license = 'BSD',
    description = """cross-platform bindings to FC-HBA APIs on Windows and Linux""",
    long_description = """cross-platform bindings to FC-HBA APIs on Windows and Linux""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'infi.cwrap',
'infi.dtypes.wwn',
'infi.instruct',
'infi.os_info',
'munch',
'setuptools'
],
    namespace_packages = ['infi'],

    package_dir = {'': 'src'},
    package_data = {'': [
'_hbaapi_aix.c'
]},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = ['hbaapi_mock = infi.hbaapi.scripts:hbaapi_mock',
'hbaapi_real = infi.hbaapi.scripts:hbaapi_real',],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    from setuptools import Extension
    import platform
    SETUP_INFO['packages'] = find_packages('src')
    if platform.system() == "AIX":
        aix_extension = Extension('infi.hbaapi.generators.hbaapi._hbaapi_aix',
            sources=['src/infi/hbaapi/generators/hbaapi/_hbaapi_aix.c'],
            libraries=['HBAAPI'])
        SETUP_INFO['ext_modules'] = [aix_extension]
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

