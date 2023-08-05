import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liquipydia",
    version="0.0.1",
    author="Benyamin Noori",
    author_email="benyamin.noori@gmail.com",
    description="Liquipydia is a python wrapper for the Liquipedia's API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/benyamin-noori/liquipydia",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)