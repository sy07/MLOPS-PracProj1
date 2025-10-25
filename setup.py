from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name = "MlOps-P1",
    version="0.1",
    author="Yash",
    packages=find_packages(),
    install_requires = requirements
)
