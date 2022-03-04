from setuptools import setup


setup(
    name='mud',
    version='0.1.0',
    author='shalst_*',
    author_email='stephenson.shane.a@gmail.com',
    packages=['mud'],
    scripts=['check.sh'],
    url='https://github.com/shalst/mudhttp://pypi.python.org/pypi/PackageName/',
    license='LICENSE',
    description='A Python package to document the modules and file structure of other Python packages',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': [
            'mud = mud.mud:main',
        ],
    }
    tests_require=['pytest'],
    install_requires=[
        "pylint",
        "pytest",
        "black",
        "coverage",
        "mypy"
    ],
)