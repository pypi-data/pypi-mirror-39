

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecoaliface",
    version="0.4.0",
    author="Mateusz Korniak",    
    author_email="matkorpypiorg@ant.gliwice.pl",
    description="Interface to eSterownik.pl eCoal water boiler controller.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matkor/ecoaliface",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta", 
    ],
)
