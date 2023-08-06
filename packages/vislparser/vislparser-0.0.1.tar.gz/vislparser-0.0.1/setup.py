import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vislparser",
    version="0.0.1",
    author="José Patrício",
    author_email="jpegx100@gmail.com",
    description="Automatic calls to VISL online parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lplnufpi/vislparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)