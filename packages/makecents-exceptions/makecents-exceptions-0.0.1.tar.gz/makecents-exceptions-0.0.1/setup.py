from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="makecents-exceptions",
    version="0.0.1",
    author="MakeCents",
    author_email="yma@mymakecents.com",
    description="exceptions package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MakeCents-NYC/makecents-exceptionst",
    packages=["makecents_exceptions"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
