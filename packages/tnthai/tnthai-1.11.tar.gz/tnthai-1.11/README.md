
# How to upload your package to PyPI 

If you haven’t published things on PyPI before, you’ll need to create an account at [PyPI](https://pypi.org/).

We need you to create an account at [TestPyPI](https://test.pypi.org/) to test before you publish your package to PyPI. (You should set username and passwords PyPI same as TestPyPI)

# Picking A Name
Python module/package names should generally follow the following constraints:

* All lowercase
* Unique on PyPI
* Underscore-separated or no word separators at all 

# Creating The Scaffolding

Directory structure for <code>tnthai</code> should look like this:
```
TnThai/
  tnthai/
    setup.py
    REAME.md
    MANIFEST.in
    bin/
      tnthai-run
      tnthai-test
    src/
      tnthai/
        __init__.py
        AbstractWordSegment.py
        SC.py
        dict/
          my.trie
        tests/
          test_tnthai.py
```
The subdirectory <code>tnthai</code> is actually our Python module

<code>setup.py</code> contains:
```Python
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='tnthai',
    version='0.1',
    description='tnthai for Python3',
    long_description=readme(),
    url='https://gitlab.thinknet.co.th/research/swathclone',
    author='Supphawit',
    author_email='supphawit@thinknet.co.th',
    license='Thinknet',
    python_requires='>=3',
    install_requires=[
        'datrie',
    ],
    scripts=['bin/tnthai-run','bin/tnthai-test'],
    keywords='tnthai thinknet thai wordsegment',
    packages=['tnthai'],
    package_dir={'tnthai': 'src/tnthai'},
    package_data={
        'tnthai': ['tests/*.py','dict/*.trie']
    },
)
```

* If your package required any package you needs to add <code>install_requires</code> keyword argument to <code>setup.py</code> 
* Many Python packages include command line tools. This is useful for distributing support tools which are associated with a library 
for <code>tnthai</code>, we will add a <code>tnthai-run</code> command line tool by adding <code>scripts</code> keyword argument 
* Package data can be added to packages using the <code>package_data</code> keyword argument to the setup() function
* Use <code>package_dir</code> key argument to path your package location
* Changed in version 3.1: All the files that match <code>package_data</code> will be added to the MANIFEST file if no template is provided. 
* You’ll probably want a README file in your source distribution, and that file can serve double purpose as the <code>long_description</code> specified to PyPI. Further, if that file is written in reStructuredText, it can be formatted nicely

see more <code>setup.py </code> in the [PyPA sample project](https://github.com/pypa/sampleproject)

The <code>tnthai-run</code> script in <code>bin/tnthai-run</code> looks like this:
```Python
#!/usr/bin/env python 

  * code *
  ...
  ...
  ...
``` 
The <code>tnthai-test</code> script in <code>bin/tnthai-test</code> use to run test for ```tnthai``` looks like this:
```Python
#!/usr/bin/env python 

import os
import sys

for p in sys.path:
    if "site-packages" in p:
        path = p + "/tnthai/tests/test_tnthai.py"
os.system("python3 " + path)
``` 

<code>MANIFEST.in</code> contains:
```
include README.md
```
If you have other files that you want to include in your package just add <code>include</code> in <code>MANIFEST.in</code> it's meaning all files in the distribution root matching *.txt,and <code>recursive-include</code> meaning all files anywhere under the <code>tnthai</code> directory matching *.txt or *.py

Now we can install the package locally (for use on our system or test before publish) with:
```
$ pip install .
```

# Publishing on TestPyPI and PyPI 

First create a source distribution with:
```
$ python setup.py sdist
```
or
```
$python3 setup.py sdist bdist_wheel
```
This will create <code>dist/tnthai-0.1.tar.gz</code> inside our top-level directory. 

You can use <code>twine</code> to upload the distribution packages. You’ll need to install <code>twine</code> by this command:
```
$ pip install twine --upgrade
```
or 
```
$ python3 -m pip install --user --upgrade twine
```

### TestPyPI
You should upload your package to TestPyPI before PyPI

Run Twine to upload all of the archives under dist:
```
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
You will be prompted for the username and password you registered with TestPyPI. 
After the command completes you can check your package at [TestPyPI](https://test.pypi.org/manage/projects/)

### PyPI
Now you ready to upload your package to PyPI
by following this command:
```
$ twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
You will be prompted for the username and password you registered with PyPI. 
After the command completes you can check your package at [PyPI](https://pypi.org/manage/projects/)

# Installing the Package

At this point, other consumers of this package can install the package with <code>pip</code>:
```
$ pip install tnthai
```
Sometimes you update your package it will take about 5-10 minutes to update your package. 

you can upgrade your package by following this command:
```
$ pip install tnthai --upgrade
```

It will be automatically installed to your Python package folder
and <code>setuptools</code> will copy the script to our PATH and make it available for general use

# How to Use
In ```tnthai``` package have 3 features ```Safe Mode```, ```Unsafe Mode```, ```Smart Mode```

You can run package in command line by following this command:
```
$ tnthai-run ทดสอบการทำงาน
```
If you want to choose the features you can do by following this command:

```
$ tnthai-run ทดสอบการทำงาน Safe
```

### Simple Demo


```
import tnthai.segment as tn


safe = tn.SafeSegment("คนแก่ขนของ")

unsafe = tn.UnsafeSegment("คนแก่ขนของ")

smart = tn.SmartSegment("คนแก่ขนของ")
```
But if you use python2 you need to add ```# -*- coding: utf-8 -*-``` like this:
```
# -*- coding: utf-8 -*-

import tnthai.segment as tnthai

  * code *
    ...
    ...
    ...
```


Result of ```Safe Mode```  will be like this:
```
('Safe', [['คนแก่', 'ขนของ'], ['คนแก่', 'ขน', 'ของ'], ['คน', 'แก่', 'ขนของ'], ['คน', 'แก่', 'ขน', 'ของ']])
```
Result of ```Unsafe Mode```  will be like this:
```
('Unsafe', [['คนแก่', 'ขนของ']])
```
To show you how its work we will show you an example:
```
import tnthai.segment as tn


misspellings_safe = tn.SafeSegment("คนแก่สขนของ")

spellings_smartmode = tn.SmartSegment("คนแก่ขนของ")

misspellings_smartmode = tn.SmartSegment("คนแก่สขนของ")
```
```Safe Mode``` doesn't work with misspellings text so the 
result will be empty list ( ```Smart Mode``` can solve this problem )

The result of ```misspellings_safe``` is:
```
('Safe', [])
```

```Smart Mode```  will automatically use ```Safe Mode```  but if its doesn't work (which mean text have misspellings) its going to use ```Unsafe Mode```  instead


The result of ```spellings_smartmode``` is:
```
('Safe', [['คนแก่', 'ขนของ'], ['คนแก่', 'ขน', 'ของ'], ['คน', 'แก่', 'ขนของ'], ['คน', 'แก่', 'ขน', 'ของ']])
```
The result of ```misspellings_smartmode``` is:
```
('Unsafe', [['คนแก่', 'ส', 'ขนของ']])
```

If you want to test package you can run ```tnthai-test``` by following this command:
```
$ tnthai-test
```
