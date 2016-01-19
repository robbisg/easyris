from setuptools import setup, find_packages
from setuptools.command.install import install
from easyris.utils import database_setup
import codecs
import os
import re
import glob


here = os.path.abspath(os.path.dirname(__file__))
def find_version(*file_paths):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print "You are installing EasyRIS!"
        database_setup.run()
        install.run(self)


setup(
    name="easyris",
    version=find_version('easyris', '__init__.py'),
    description="EasyRIS by Serve",


    # The project URL.
    url='https://www.ser-ve.it/',

    # Author details
    author='Serve',
    author_email='info@ser-ve.it',

    # Choose your license
    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='ris clinic data',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages.
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed.
    install_requires = ['pymongo', 
                        'mongoengine', 
                        'flask-security', 
                        'flask-mongoengine', 
                        'flask-cors',
                        #'nibabel'
                        ],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    #package_data={
    #   'sample': ['package_data.dat'],
    #},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    
    # data_files=[('utils/files', glob.glob('utils/files/*.csv'))],
    
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.

    cmdclass={
        'database': CustomInstallCommand,
        #'develop': CustomInstallCommand,
    },
    #scripts = ['scripts/patient_db.py']
)
