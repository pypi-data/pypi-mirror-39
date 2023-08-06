import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    REQUIRES = fh.read().split("\n")

setuptools.setup(
    name="feature_mining",
    version="0.0.5",
    author="H. Wilder, N. Freundlich, Santu Karmaker",
    author_email="hwilder3@illinois.edu, norbert4@illinois.edu, karmake2@illinois.edu",
    description="Mine implicit features using a generative feature language model.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
