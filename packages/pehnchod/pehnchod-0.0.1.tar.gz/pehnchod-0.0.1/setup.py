import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pehnchod",
    version="0.0.1",
    author="Karanveer Singh",
    author_email="singh.karanv@gmail.com",
    description="Test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gobigrinder/py-lib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
