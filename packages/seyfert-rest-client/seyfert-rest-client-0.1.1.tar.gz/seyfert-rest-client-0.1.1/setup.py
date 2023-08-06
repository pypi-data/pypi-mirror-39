import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seyfert-rest-client",
    version="0.1.1",
    author="bartkim0426",
    author_email="bartkim0426@gmail.com",
    description="REST client for seyfert wth python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/bartkim0426/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
