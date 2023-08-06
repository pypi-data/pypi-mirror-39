import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knnmv",
    install_requires=[
        'numpy',
        'scikit-learn'
    ],
    version="0.0.2",
    author="Massimo Belloni",
    author_email="massibelloni@gmail.com",
    description="Sparsity aware KNN imputation.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/massibelloni/knnmv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)