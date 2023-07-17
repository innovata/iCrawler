# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipycrawl",
    version="0.0.9",
    author="innovata",
    author_email="iinnovata@gmail.com",
    description='Web Crawlling, Scrapying 또는 OpenAPI 를 사용하여 데이타를 수집하는 Innovata-Crawler',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/iCrawler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages('src'),
    python_requires=">=3.8",
)
