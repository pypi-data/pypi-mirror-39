import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cnf",
    version="0.0.4",
    author="Sumner Magruder",
    author_email="sumner.magruder@zmnh.uni-hamburg.de",
    description="Simple Conjunctive Normal Filter for python3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SumNeuron/cnf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True

)
