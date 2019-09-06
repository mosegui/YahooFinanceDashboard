import setuptools

setuptools.setup(
     name='mahalanobis',
     version='0.1',
     packages=setuptools.find_packages(),
     author="Daniel Moseguí González",
     author_email="d.mosegui@gmail.com",
     description="Package for performing calculations of Mahalanobis distances",
     url="https://github.com/mosegui/mahalanobis",
     classifiers=[
	 "Programming Language :: Python :: 3"
         "Programming Language :: Python :: 3.6",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YahooFinanceDashboard",
    version="0.0.1",
    author="Daniel Moseguí González",
    author_email="d.mosegui@gmail.com",
    description="API for accessing, synchronizing, managing locally and plotting Yahoo financial data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)