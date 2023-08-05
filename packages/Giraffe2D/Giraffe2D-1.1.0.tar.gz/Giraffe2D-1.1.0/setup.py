import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Giraffe2D",
    version="1.1.0",
    author="Saugat Siddiky Jarif",
    author_email="saugatjarif@gmail.com",
    description="Simple Pygame Powered Game Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrypticCoding/Girrafee2D",
    package_dir={'': 'Engine'}
)
