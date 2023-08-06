import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vrypy",
    version="0.3",
    author="Vojtech Rylko",
    author_email="vojta.rylko@gmail.com",
    description="Collection of Python utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vojtarylko/vrypy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
