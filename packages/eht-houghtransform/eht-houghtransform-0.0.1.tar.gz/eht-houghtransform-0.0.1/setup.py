import setuptools
from setuptools import setup
 
setup(
    name="eht-houghtransform",
    version="0.0.1",
    author="Joseph Farah",
    author_email="joseph.farah@cfa.harvard.edu",
    description="Hough transform package, created and distributed by SAO-EHT",
    long_description="Hough transform package, created and distributed by SAO_EHT",
    long_description_content_type="text/markdown",
    url="https://github.com/sao-eht/HoughTransform",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
    ],
)
