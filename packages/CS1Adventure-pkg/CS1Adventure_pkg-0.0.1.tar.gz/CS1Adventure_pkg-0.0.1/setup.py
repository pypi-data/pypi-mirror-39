import setuptools

with open("README.md", "r") as fh:
    long_description=fh.read()

setuptools.setup(
    name="CS1Adventure_pkg",
    version ="0.0.1",
    author="Group 2",
    author_email="author@example.com",
    description="A test for the text adventure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnRubado/cs370-Text-Engine-2",
    packages=setuptools.find_packages(),
    classifiers =[

    ],
    )
