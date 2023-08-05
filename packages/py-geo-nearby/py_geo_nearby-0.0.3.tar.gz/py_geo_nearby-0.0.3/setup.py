import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_geo_nearby",
    version="0.0.3",
    author="Harinath Selvaraj",
    author_email="harinath.selvaraj@outlook.com",
    description="Python library to arrange geo locations by nearest distance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harinathselvaraj/py_geo_nearby",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
