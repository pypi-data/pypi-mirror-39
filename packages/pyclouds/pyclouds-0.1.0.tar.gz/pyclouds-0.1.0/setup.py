from distutils.core import setup

setup(
    name = 'pyclouds',
    version = '0.1.0',
    description = 'Project in development',
    author = 'Wasim',
    author_email = 'wasim@thabraze.me',
    url = 'https://github.com/waseem18/pyclouds',
    py_modules=['pyclouds'],
    install_requires=[
        # list of this package dependencies
    ],
    entry_points='''
        [console_scripts]
        pyclouds=pyclouds:cli
    ''',
)
