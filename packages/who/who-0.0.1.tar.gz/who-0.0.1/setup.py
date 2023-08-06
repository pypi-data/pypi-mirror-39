import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="who",
    version="0.0.1",
    author="Sweeterio",
    author_email="sweeterio@qq.com",
    description="Who are you",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sweeterio/who",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)