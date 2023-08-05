import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

install_requires = ['pytest']

setuptools.setup(
    name="advent-of-code-helpers",
    version="0.0.4",
    author="Marcus Vaal",
    license="MIT",
    description="Advent of Code helper functions",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mvaal/advent-of-code-helpers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=install_requires
)
