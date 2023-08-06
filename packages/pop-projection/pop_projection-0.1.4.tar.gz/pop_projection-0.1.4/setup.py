import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pop_projection",
    version="0.1.4",
    author="Amine TEFFAL",
    author_email="a.teffal@gmail.com",
    description="Projection of population of a retirement plan.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ateffal/pop_projection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)