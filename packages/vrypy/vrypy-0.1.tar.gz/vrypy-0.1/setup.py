import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vrypy",
    version="0.1",
    author="Vojtech Rylko",
    author_email="vojta.rylko@gmail.com",
    description="Collection of Python utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vrycz/vrypy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
