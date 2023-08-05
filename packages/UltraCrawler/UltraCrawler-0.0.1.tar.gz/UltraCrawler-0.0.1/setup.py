import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UltraCrawler",
    version="0.0.1",
    author="Appx",
    author_email="appx@outlook.com",
    description="Ultra Crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.appx.xyz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)