# coding: utf-8
import codecs

from setuptools import setup, find_packages

package_name = "kin-base"

exec(open("kin_base/version.py").read())

with codecs.open('README.rst', encoding='utf-8') as file:
    long_description = file.read()

tests_require = ['pytest', 'mock']

with open('requirements.txt') as f:
    requires = [line.split(' ')[0] for line in f]

setup(
    name=package_name,
    version=__version__,
    description='Code for managing Stellar.org blockchain transactions and accounts using stellar-base in python. Allows full functionality interfacing with the Horizon front end. Visit https://stellar.org for more information.',
    long_description=long_description,
    keywords=["stellar.org", "lumens", "xlm", "blockchain", "distributed exchange", "cryptocurrency", "dex",
              "stellar-core", "horizon", "sdex", "trading"],
    url='https://github.com/kinecosystem/py-kin-base/',
    license='Apache',
    author='Eno, overcat',
    author_email='appweb.cn@gmail.com, 4catcode@gmail.com',
    maintainer='Ron Serruya',
    maintainer_email='ron.serruya@kik.com',
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=requires,
    tests_require=tests_require
)
