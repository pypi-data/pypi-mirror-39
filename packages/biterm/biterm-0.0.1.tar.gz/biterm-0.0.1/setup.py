import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biterm",
    version="0.0.1",
    author="markoarnauto",
    author_email="markustretzmueller@gmail.com",
    description="Biterm Topic Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/markoarnauto/biterm",
    packages=setuptools.find_packages(exclude=['biterm.example']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)