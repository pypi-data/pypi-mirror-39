import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="asrtt",
    version="0.0.3",
    author="Albert",
    description="An automated time tracker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/albertsgrc/asrtt-client",
    py_modules=['asrtt', 'configstore', 'utils'],
    install_requires=[
        'pynput==1.4',
        'logzero==1.5.0',
        'click==6.7',
        'requests>=2.20.0',
        'gitpython==2.1.11',
        'inquirer==2.5.1',
        'validators==0.12.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points='''
        [console_scripts]
        asrtt=asrtt:main
   ''',
)
