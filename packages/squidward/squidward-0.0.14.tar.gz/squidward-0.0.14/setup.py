import setuptools

# python3 -m pip install --user --upgrade setuptools wheel
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# python3 -m pip install squidward

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="squidward",
    version="0.0.14",
    author="James Montgomery",
    author_email="looyclark@gmail.com",
    description="Package for implementing Gaussian Process models in python 2/3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/looyclark/squidward",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.15.1',
        'scipy>=1.1.0',
        'matplotlib>=2.2.3',
        'seaborn>=0.9.0',
        'nose>=1.3.7',
        'pylint>=1.8.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
