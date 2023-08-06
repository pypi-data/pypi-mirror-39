import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="selsunpool",
    version="0.0.2",
    author="nicholishen",
    author_email="nicholishen@tutanota.com",
    description="A local selenium pool executor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nicholishen/selsunpool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "selenium"
    ],
)