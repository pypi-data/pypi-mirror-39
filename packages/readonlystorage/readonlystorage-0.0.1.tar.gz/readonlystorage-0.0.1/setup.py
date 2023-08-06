import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="readonlystorage",
    version="0.0.1",
    author="Yaal",
    author_email="contact@yaal.fr",
    description="A readonly wrapper around a ZODB storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/yaal/readonlystorage",
    packages=setuptools.find_packages(),
    install_requires=['ZODB'],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
