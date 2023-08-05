import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seabred",
    version="0.0.1",
    author="Julia Ebert",
    author_email="julia@juliaebert.com",
    description="Seaborn-like plots for numpy arrays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jtebert/seabred",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib'
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
