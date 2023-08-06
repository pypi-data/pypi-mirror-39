import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodiff_jel",
    version="0.0.4",
    author="Team JEL",
    author_email="",
    description="Python library for Automatic Differentiation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teamjel/cs207-FinalProject",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "graphviz"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)