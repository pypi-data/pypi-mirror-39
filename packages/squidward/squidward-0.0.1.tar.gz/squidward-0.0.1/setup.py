import setuptools 
# https://packaging.python.org/tutorials/packaging-projects/

# python3 -m pip install --user --upgrade setuptools wheel
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="squidward",
    version="0.0.1",
    author="James Montgomery",
    author_email="looyclark@gmail.com",
    description="Package for implementing Gaussian Process models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/looyclark/squidward",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.15.1',
        'scipy>=1.1.0',
        'matplotlib>=2.2.3',
        'seaborn>=0.9.0',
        'nose>=1.3.7'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
