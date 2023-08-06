from distutils.core import setup

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name="Giraffe2D",
    version="1.1.7",
    packages=['Engine'],
    #package_dir = {'': 'Engine'},
    author="Saugat Siddiky Jarif",
    author_email="saugatjarif@gmail.com",
    description="Simple Pygame Powered Game Engine",
    url="https://github.com/CrypticCoding/Girrafee2D"
    
)
