import config
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read().replace("ParaCode", config.language_name)

setuptools.setup(
    name=config.language_name,
    version=config.version,
    author=config.author,
    author_email="darubyminer360@gmail.com",
    description="The " + config.language_name + " Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaRubyMiner360/ParaCode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)