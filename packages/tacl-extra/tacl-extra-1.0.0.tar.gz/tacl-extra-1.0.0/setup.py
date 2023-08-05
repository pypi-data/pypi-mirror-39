from setuptools import setup


with open('README.rst') as fh:
    long_description = fh.read()

setup(
    name='tacl-extra',
    version='1.0.0',
    description='Collection of scripts to generate various TACL results '
    'and reports',
    long_description=long_description,
    author='Jamie Norrish',
    author_email='jamie@artefact.org.nz',
    url='https://github.com/ajenhl/tacl-extra',
    project_urls={
        'Source': 'https://github.com/ajenhl/tacl-extra',
        'Tracker': 'https://github.com/ajenhl/tacl-extra/issues',
    },
    python_requires='~=3.5',
    license='GPLv3+',
    packages=['taclextra', 'taclextra.cli'],
    entry_points={
        'console_scripts': [
            'int-all=taclextra.cli.int_all:main',
            'jitc=taclextra.cli.jitc:main',
            'lifetime=taclextra.cli.lifetime:main',
            'paternity=taclextra.cli.paternity:main',
        ],
    },
    package_data={
        'taclextra': ['assets/jitc/*.css', 'assets/jitc/*.js',
                      'assets/templates/*.html'],
    },
    test_suite='tests',
    install_requires=['tacl>=4.2.0'],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Linguistic',
    ],
)
