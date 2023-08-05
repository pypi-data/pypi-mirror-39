import setuptools

with open("README.md", "r") as f:
    long_desciption = f.read()

setuptools.setup(
    name="pyconverter",
    version="0.0.2",
    author="soyouzpanda",
    author_email="petitpanda140@gmail.com",
    description="A package to convert type format "
                "(binary, float, double, decimal, hexadecimal, octal, utf8, utf16) to another",
    long_description=long_desciption,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
