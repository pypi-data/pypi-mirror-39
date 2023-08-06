import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cardinality_cs110",
    version="0.0.8",
    author="Abdul Qadir",
    author_email="abdul.qadir@minerva.kgi",
    description="A cardinality estimator using the Flajolet-Martin algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DarthQadir/cardinality_cs110.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)