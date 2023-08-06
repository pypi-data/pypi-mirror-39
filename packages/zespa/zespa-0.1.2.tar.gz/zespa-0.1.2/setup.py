from setuptools import setup

SHORT_DESCRIPTION = """
A tool to aggregate issues's story-point(estimate) by labels and time from ZenHub""".strip()

DEPENDENCIES = [
    'beautifultable==0.5.3',
    'fire==0.1.2',
    'requests>=2.20.0',
    'tqdm',
]

TEST_DEPENDENCIES = [
]

VERSION = '0.1.2'
URL = 'https://github.com/showwin/ZenHub-SP-Aggregator'

setup(
    name='zespa',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    url=URL,

    author='showwin',
    author_email='showwin_kmc@yahoo.co.jp',
    license='Apache Software License',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    entry_points={
        'console_scripts': 'zespa = zespa.main:main'
    },

    keywords='ZenHub issue aggregate storypoint estimate',

    packages=['zespa'],

    install_requires=DEPENDENCIES,
    tests_require=TEST_DEPENDENCIES,
)
