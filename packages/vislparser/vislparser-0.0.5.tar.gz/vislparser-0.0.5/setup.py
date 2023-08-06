import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_requires():
    req = list()
    with open("vislparser/requirements.pip", "r") as arq:
        for line in arq.read().splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                req.append(line)
    return req

setuptools.setup(
    name="vislparser",
    version="0.0.5",
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
    install_requires=list(get_requires())
)