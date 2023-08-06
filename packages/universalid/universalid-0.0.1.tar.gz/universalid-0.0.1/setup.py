import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="universalid",
    version="0.0.1",
    author="Jakob Majkilde",
    author_email="jakob@mjakilde.dk",
    description="UUID with built-in creation date",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/majkilde/universalid.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)