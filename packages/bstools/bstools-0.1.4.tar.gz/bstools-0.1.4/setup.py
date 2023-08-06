import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bstools",
    version="0.1.4",
    author="Bernie Suen",
    author_email="bernie.suen@outlook.com",
    description="some very useful tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qkjs/bstools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)