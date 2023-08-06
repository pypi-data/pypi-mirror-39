import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hyvebrain",
    version="1.0.1",
    author="Tegan Burns",
    author_email="python@hyvebrain.com",
    description="Hyvebrain API Client Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hyvebrain.com/",
    packages=setuptools.find_packages(),
)
