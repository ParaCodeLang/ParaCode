import config
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paracode-DaRubyMiner360", # Replace with your own username
    version=config.version,
    author=config.author,
    author_email="darubyminer360@gmail.com",
    description="The ParaCode Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/darubyminer360/paracode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)