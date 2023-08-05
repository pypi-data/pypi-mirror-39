#from distutils.core import setup
from setuptools import setup

#f = open('README.md')
long_description = '''
<img src="gallery-keif-snow.jpg" align="right" />

Integrating sphere how to Readme
================================


[![License MIT](http://img.shields.io/badge/license-MIT-brightgreen.svg)](license.md)
[![Version](http://img.shields.io/badge/version-2.2-brightgreen.svg)](https://gitlab.com/fabriziodifran/esfera-codigo-verilog/blob/master/Menu_frontend.py)

## Author(s)
*   Victor Esparza
*   Fabrizio Di Francesco
--------------------------------------------------------------------------------
## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on your system.

--------------------------------------------------------------------------------
### Prerequisites

What things you need to install the software and how to install them:

*   Python 2.7 and or 3.7.1 (latest version)
*   pip (latest version)
The rest of the needed packages is going to be installed as a dependency from pip repo.
--------------------------------------------------------------------------------

## Installing process

Navigate to pip repo [pip](https://pypi.org/project/iteda/)

All you need is to execute the command displayed in your favourite terminal.


### Using Iteda software (Unix/Linux/Windows/MacOS)

`Unix/Linux`

    open a terminal
    cd ~/.local/lib/python2.7/site-packages/iteda  ## this might change depending on the version you are executing
    python iteda.py  ## if you need to see the help add -h to the command

`Windows`

    open a terminal
    cd C:\Python27\Lib\site-packages\iteda ## this might change depending on the version you are executing
    python iteda.py  ## if you need to see the help add -h to the command

`MacOS`

    open a terminal
    cd ~/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/iteda  ## this might change depending on the version you are executing
    python iteda.py  ## if you need to see the help add -h to the command

## Versioning

We use [GitKraken](https://www.gitkraken.com) for versioning.

## Acknowledgments

* A big thank you to all the iteda team
'''

setup(
  name = 'iteda',         # How you named your package folder (MyLib)
  packages = ['iteda'],   # Chose the same as "name"
  version = '0.9.1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is a menu to control an integrating sphere through a serial interface (rs232)',   # Give a short description about your library
  #long_description=read('README.rst'),
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'victor esparza',                   # Type in your name
  author_email = 'vicmaresparza@gmail.com',      # Type in your E-Mail
  url = 'https://gitlab.com/fabriziodifran/esfera-codigo-verilog',   # Provide either the link to your github or to your website
  #download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['MENU', 'UART', 'SPHERE'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
          'numpy',
          'pyserial',
          'argparse',
          'serial',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 2.7',      #Specify which pyhton versions that you want to support
  ],
)