# from setuptools import setup, find_packages
# setup(
#     name="autodiff",
#     version="0.1",
#     packages=find_packages('autodiff'),
#     package_dir={"":"autodiff"}
# )
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyautodiff",
    version="0.1.1",
    author="Phoebe Wong",
    author_email="wong@g.harvard.edu",
    description="A package for automatic differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cs207-group2/cs207-FinalProject",
    packages=find_packages('autodiff'),
    package_dir = {"":"autodiff"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
