import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libFTP",
    version="0.4",
    author="blueboxdev",
    author_email="thanakorn.vsalab@gmail.com",
    description="A small example package FTP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bluebox-dev/libFTP",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
