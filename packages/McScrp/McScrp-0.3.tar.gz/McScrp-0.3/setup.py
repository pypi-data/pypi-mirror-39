import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="McScrp",
    version="0.3",
    author="CHAHBOUN Mohammed",
    author_email="simomega42@gmail.com",
    description="Simple Scrapping Library",
    long_description=long_description,
    url="https://github.com/Medpy/McScraping",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)