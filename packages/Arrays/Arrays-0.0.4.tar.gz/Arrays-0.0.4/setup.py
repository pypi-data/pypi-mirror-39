import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Arrays",
    version="0.0.4",
    author="RedDog",
    author_email="bremo.lincolin101@gmail.com",
    description="Python library for storing and reading stored arrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/S0FTY/Arrays",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
