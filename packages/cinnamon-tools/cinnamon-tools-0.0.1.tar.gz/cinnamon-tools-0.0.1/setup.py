import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cinnamon-tools",
    version="0.0.1",
    author="Caleb Mennen",
    author_email="pip@calebmennen.com",
    description="A small library of personal utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cmennen/library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
