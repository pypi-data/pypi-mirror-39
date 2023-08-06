import setuptools
import weichigong

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=weichigong.__name__,
    version=weichigong.__version__,
    author=weichigong.__author__,
    author_email=weichigong.__author_email__,
    description="a centralized configuration library based on zookeeper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/perfeelab/weichigong",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
