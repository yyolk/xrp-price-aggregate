"""
 ▄▀▀▄ ▀▀▄  ▄▀▀▀▀▄   ▄▀▀▀▀▄      ▄▀▀▄ █ 
█   ▀▄ ▄▀ █      █ █    █      █  █ ▄▀ 
▐     █   █      █ ▐    █      ▐  █▀▄  
      █   ▀▄    ▄▀     █         █   █ 
    ▄▀      ▀▀▀▀     ▄▀▄▄▄▄▄▄▀ ▄▀   █  
    █                █         █    ▐  
    ▐                ▐         ▐  

xrp-price-aggregate setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README
long_description = (here / "README.md").read_text(encoding="utf-8")
# Get the install_requires from requirements.txt
install_requires = (here / "requirements.txt").read_text(encoding="utf-8").splitlines()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="xrp-price-aggregate",
    version="0.0.1",
    description=(
        "A utility library that wraps grabbing the current spot price"
        " of $XRP from various exchanges."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yyolk/xrp-price-aggregate",
    author="Joseph Chiocchi",
    author_email="joe@yolk.cc",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish
        "License :: OSI Approved :: ISC License (ISCL)",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="xrp, xrpl, ccxt, cryptocurrency",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=install_requires,
    project_urls={
        "Bug Reports": "https://github.com/yyolk/xrp-price-aggregate/issues",
        "Source": "https://github.com/yyolk/xrp-price-aggregate/",
    },
)
