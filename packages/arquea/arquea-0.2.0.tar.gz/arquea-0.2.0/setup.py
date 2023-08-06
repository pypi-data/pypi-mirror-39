import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arquea",
    version="0.2.0",
    author="Gabriel Lasaro",
    author_email="gabriellasarosaleze@gmail.com",
    description="Um pequeno banco de dados NoSQL feito em Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gabriellasaro.github.io/arqueadb/",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
