import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rm_logger",
    version="0.0.1",
    author="Chris O'Brien",
    author_email="christopher.obrien@remindermedia.com",
    description="A generic logging class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
    ],
)
