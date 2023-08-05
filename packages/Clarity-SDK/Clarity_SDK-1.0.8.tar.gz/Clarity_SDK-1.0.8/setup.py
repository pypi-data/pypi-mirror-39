import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Clarity_SDK",
    version="1.0.8",
    author="Intuli",
    author_email="intuli.developer@gmail.com",
    description="Python SDK for the Clarity API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://test.pypi.org/legacy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
