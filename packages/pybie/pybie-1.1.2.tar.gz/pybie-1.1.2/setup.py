import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybie",
    version="1.1.2",
    author="Obie",
    author_email="obyaltha@example.com",
    description="A very simple web frameword for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Robialta/pybie",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)