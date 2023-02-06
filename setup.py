import io
import re

import setuptools

VERSION_FILE = "lintlizard/__init__.py"
with io.open(VERSION_FILE, "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = ([\'"])(.*?)\1', f.read()).group(2)

setuptools.setup(
    name="lintlizard",
    version=version,
    author="Vyacheslav Tverskoy",
    author_email="v@close.com",
    description="Run various linters to ensure a common code quality baseline",
    url="https://github.com/closeio/lintlizard",
    packages=setuptools.find_packages(),
    install_requires=[
        'attrs',
        'black==22.12.0',
        'flake8==5.0.4',
        'flake8-bugbear==23.1.14',
        'flake8-comprehensions==3.10.1',
        'flake8-docstrings==1.6.0',
        'flake8-no-u-prefixed-strings==0.2',
        'flake8-polyfill==1.0.2',
        'flake8-tidy-imports==4.8.0',
        'flake8-sfs==0.0.4',
        'flake8-simplify==0.19.3',
        'isort==5.11.3',
        'mccabe==0.7.0',
        'mdformat==0.7.16',
        'mypy==0.990',
        'mypy-extensions==1.0.0',
        'pathspec==0.10.3',
        'pep8==1.7.1',
        'pep8-naming==0.13.3',
        'pycodestyle==2.9.1',
        'pydocstyle==6.1.1',
        'pyflakes==2.5.0',
        'snowballstemmer==2.2.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'lintlizard=lintlizard:main',
        ],
    },
)
