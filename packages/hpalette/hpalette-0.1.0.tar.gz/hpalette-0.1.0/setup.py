import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hpalette",
    version="0.1.0",
    author="Saketh Rama",
    author_email="rama@seas.harvard.edu",
    description="Library of color palettes for Harvard identity guidelines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saketh/hpalette",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Education",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
