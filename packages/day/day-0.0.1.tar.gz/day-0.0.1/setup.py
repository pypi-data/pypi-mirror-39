import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="day",
    version="0.0.1",
    author="Sweeterio",
    author_email="sweeterio@qq.com",
    description="what's day is today",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sweeterio/day",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)