from setuptools import find_packages, setup

setup(
    name='brewblox-datastore',
    use_scm_version={'local_scheme': lambda v: ''},
    description='REST endpoints for editing a JSON file',
    long_description=open('README.md').read(),
    url='https://github.com/BrewBlox/brewblox-datastore',
    author='BrewPi',
    author_email='development@brewpi.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware',
    ],
    keywords='brewing brewpi brewblox embedded plugin service',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'brewblox-service~=0.14.0',
        'aiofiles~=0.3.2',
    ],
    python_requires='>=3.7',
    setup_requires=['setuptools_scm'],
)
