import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x448-python",
    version="1.0.0",
    author="Piotr Lizonczyk",
    author_email="plizonczyk.public@gmail.com",
    description="Pure Python3 implementation of x448.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/plizonczyk/x448-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
