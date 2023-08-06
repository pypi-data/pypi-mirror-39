import pathlib

from setuptools import setup

# Folder containing this file.
HERE = pathlib.Path(__file__).parent

README = (HERE.joinpath("README.MD")).read_text()

setup(
    name="markdown-iconfonts",
    description="Easily display icon fonts in markdown.",
    long_description=README,
    long_description_content_type="text/markdown",
    version="3.0.0",
    py_modules=["iconfonts"],
    install_requires=["markdown"],
    author="Eric Eastwood",
    url="https://github.com/MadLittleMods/markdown-icons",
    keywords="markdown, icons, fontawesome, bootstrap",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ]
)
