import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lzdb",
    version="0.0.8",
    author="moenova",
    author_email="author@example.com",
    description="An easy local database for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moenova/lazy-database",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
