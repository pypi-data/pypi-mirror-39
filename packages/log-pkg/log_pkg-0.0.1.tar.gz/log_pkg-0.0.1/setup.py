import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="log_pkg",
    version="0.0.1",
    author="Tinywan",
    author_email="756684177@qq.com",
    description="A small log package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tinywan/log_pkg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)