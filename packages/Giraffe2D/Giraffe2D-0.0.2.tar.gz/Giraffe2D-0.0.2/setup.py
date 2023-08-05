import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Giraffe2D",
    version="0.0.2",
    author = "Saugat Siddiky Jarif",
    author_email="saugatjarif@gmail.com",
    description="Simple Python And OpenGL Powered Game Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrypticCoding/Girrafee2D",
    packages=setuptools.find_packages(),
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
