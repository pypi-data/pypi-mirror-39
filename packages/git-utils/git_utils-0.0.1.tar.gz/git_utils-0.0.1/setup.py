import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git_utils",
    version="0.0.1",
    author="Luis Cruz",
    author_email="luismirandacruz@gmail.com",
    description="Extension of the library gitpython.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luiscruz/git_utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)