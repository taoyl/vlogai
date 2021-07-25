# vlogai
A python package for verilog auto instantiation

# Features

  - Auto instantiation for verilog modules
  - Support macros and paramaters with all verilog formats
  - Update instantiations based on value changes of paramaters and macros
  - Support directives for auto declaring wires and external ports without duplicated declaraions
  - Support instport changes using python regexp
  - Support individual file, file list and incdir search for finding module definitions
  - Support systemverilog interface bundle for instantiations
  - Support individual file, file list and incdir search for expanding interface bundles.


# Installation
## Requirements
This package requires Python 3.6 or later (3.7 is better) and pyverilog(>=1.2.0)(https://github.com/PyHDI/Pyverilog).

```
pip3 install pyverilog
```

Note: Python 3.7 is better because it keeps the ordering of dict items when inserted.

## Install with pip
You can use the following to install vlogai package.

```
pip3 install git+https://github.com/taoyl/vlogai.git
```

To upgrade vlogai, use the following command:

```
pip3 install --upgrade git+https://github.com/taoyl/vlogai.git
```

## Manual installation
If you don't have pip installed, I suggest you to install it first :)
If you would really like to install vlogai manually, please try the following:

```
git clone https://github.com/taoyl/vlogai.git
cd vlogai
python3 setup.py install
``` 

# Reference Usage:
1. Used as a python pakcage, please refer to demos.
2. Used in vim as plugin, please refer to https://github.com/taoyl/vim-vlogautoinst
