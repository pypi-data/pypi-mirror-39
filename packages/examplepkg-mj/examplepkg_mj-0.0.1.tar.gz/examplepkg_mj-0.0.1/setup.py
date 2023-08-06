import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="examplepkg_mj",
    version="0.0.1",
    author="Minjong Kim",
    author_email="minjong.kim@gmail.com",
    description="An example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soundpainter/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
