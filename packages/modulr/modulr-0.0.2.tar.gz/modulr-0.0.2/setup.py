import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modulr",
    version="0.0.2",
    author="Martin Skarzynski",
    author_email="marskar@gmail.com",
    description="Save currently defined classes and functions to modules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marskar/modulr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
