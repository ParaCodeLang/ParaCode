import setuptools

language_name = "ParaCode"
author = "DaRubyMiner360"
version = "1.1.2"

with open("README.md", "r") as fh:
    long_description = fh.read().replace("ParaCode", language_name)

setuptools.setup(
    name=language_name,
    version=version,
    author=author,
    author_email="darubyminer360@gmail.com",
    description="The " + language_name + " Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ParaCodeLang/ParaCode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)