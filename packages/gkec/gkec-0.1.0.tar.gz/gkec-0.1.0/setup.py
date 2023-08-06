import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gkec",
    version="0.1.0",
    author="Sergio Perez",
    author_email="sergiopr89@gmail.com",
    description="A simple client to operate with GKE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/cattlelizers.io/gkec",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=[
        "google-api-python-client",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
