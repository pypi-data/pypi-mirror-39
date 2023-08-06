import re
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = re.search(
    r'^__version__\s*=\s*"(.*)"',
    open('whodis/__init__.py').read(),
    re.M
).group(1)

setuptools.setup(
    name="whodis",
    version=VERSION,
    author="Josh Campbell",
    author_email="josh@userdel.com",
    description="Parses the contents of a source code directory and "
                "determines the programming languages in use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/irlrobot/whodis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
