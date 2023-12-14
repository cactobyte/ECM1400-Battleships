import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="battleships-boris",
    version="0.0.1",
    author="Boris Cheung",
    author_email="bybc201@exeter.ac.uk",
    long_description = long_description,
    description = "A battleship game made with Py"

)