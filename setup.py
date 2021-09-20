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
        'black==21.9b0',
        'flake8==3.9.2',
        'flake8-bugbear==21.9.1',
        'flake8-docstrings==1.6.0',
        'flake8-future-import==0.4.6',
        'flake8-no-u-prefixed-strings==0.2',
        'flake8-polyfill==1.0.2',
        'flake8-tidy-imports==4.4.1',
        'flake8-sfs==0.0.3',
        'flake8-simplify==0.14.1',
        'isort==5.9.3',
        'mccabe==0.6.1',
        'mypy==0.910',
        'mypy-extensions==0.4.3',
        'pathspec==0.9.0',
        'pep8==1.7.1',
        'pep8-naming==0.12.1',
        'pycodestyle==2.7.0',
        'pydocstyle==6.1.1',
        'pyflakes==2.3.1',
        'snowballstemmer==2.1.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'lintlizard=lintlizard:main',
        ],
    },
)
