import setuptools
from pkg_resources import parse_requirements

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name="pyaxonaut",
    version="0.0.1",
    author="AJ Innov",
    author_email="contact@ajinov.fr",
    description="A non official API wrapper for Axonaut CRM",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antoine-briand/pyaxonaut",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
