from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pauli",
    version="0.0.1",
    license="MIT",
    author="Swellaby",
    author_email="opensource@example.com",
    description="Utility for managing Azure Pipelines components in bulk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swellaby/pauli",
    packages=find_packages(),
)
