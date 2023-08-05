import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="advent-of-code-helpers",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    license="MIT",
    description="Advent of Code helper functions",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries"
    ]
)
