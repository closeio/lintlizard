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
        'black==20.8b1',
        'flake8==3.9.1',
        'flake8-bugbear==21.4.3',
        'flake8-docstrings==1.6.0',
        'flake8-future-import==0.4.6',
        'flake8-no-u-prefixed-strings==0.2',
        'flake8-polyfill==1.0.2',
        'flake8-tidy-imports==4.2.1',
        'isort==5.8.0',
        'mccabe==0.6.1',
        'mypy==0.812',
        'mypy-extensions==0.4.3',
        'pathspec==0.8.1',
        'pep8==1.7.1',
        'pep8-naming==0.11.1',
        'pycodestyle==2.7.0',
        'pydocstyle==6.0.0',
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
