import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="catpictures",
    version="1.1",
    author="Giacomo Lawrance",
    author_email="thenerdystudent@gmail.com",
    description="Open a picture of a cat in a new tab on your browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GiacomoLaw/catpictures",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)