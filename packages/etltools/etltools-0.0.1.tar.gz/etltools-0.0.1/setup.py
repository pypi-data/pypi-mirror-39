import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="etltools",
    version="0.0.1",
    author="quzhengpeng",
    author_email="quzhengpeng@163.com",
    maintainer="quzhengpeng",
    maintainer_email="quzhengpeng@163.com",
    description="A etl tool for DW",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD License",
    url="https://github.com/quzhengpeng/etltools",
    packages=setuptools.find_packages(),
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy>=1.14.3'
    ]
)
