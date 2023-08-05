import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sentenceslug",
    version="1.1",
    author="jef79m",
    author_email="jeff@fuzzknuckle.com",
    description="Generate random slugs using basic sentence structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jef79m/sentenceslug",
    keywords=["random", "slug", "sentence"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
