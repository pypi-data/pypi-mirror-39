import setuptools
from collections import OrderedDict

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bstools",
    version=__import__('bstools').__version__,
    author="Bernie Suen",
    author_email="bernie.suen@outlook.com",
    description="some very useful tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qkjs/bstools",
    project_urls=OrderedDict((
        ('Documentation', 'https://github.com/pallets/flask'),
        ('Code', 'https://github.com/pallets/flask'),
        ('Issue tracker', 'https://github.com/pallets/flask'),
    )),
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)