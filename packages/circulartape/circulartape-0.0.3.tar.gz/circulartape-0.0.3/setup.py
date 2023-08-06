from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="circulartape",
    version="0.0.3",
    description="A circular linked list implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tris Emmy Wilson",
    author_email="anemptystring@gmail.com",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
