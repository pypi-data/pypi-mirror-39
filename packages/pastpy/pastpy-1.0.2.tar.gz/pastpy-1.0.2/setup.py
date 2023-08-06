from codecs import open
import os.path

from setuptools import setup, find_packages

MY_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

# with open(os.path.join(MY_DIR_PATH, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()

root_package_dir_path = os.path.join(MY_DIR_PATH, "src", "pastpy")
package_data = []
for dir_path, subdir_names, _file_names in os.walk(os.path.join(root_package_dir_path, "site", "template")):
    package_data.append(os.path.relpath(
        dir_path, root_package_dir_path).replace(os.path.sep, "/") + "/*")

setup(
    author='Minor Gordon',
    author_email='pastpy@minorgordon.net',
    name='pastpy',
    description='Python library for working with PastPerfect databases',
    license='BSD',
    # long_description=long_description,
    url='https://github.com/minorg/pastpy',
    version='1.0.2',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3'
    ],

    entry_points={
        'console_scripts': ['pastpy=pastpy.cli:main'],
    },

    install_requires=('beautifulsoup4', 'dbf', 'enum34', 'pystache'),

    # What does your project relate to?
    keywords='pastperfect',

    packages=find_packages("src"),
    package_data={"": package_data},
    package_dir={'pastpy': 'src/pastpy'},
)
