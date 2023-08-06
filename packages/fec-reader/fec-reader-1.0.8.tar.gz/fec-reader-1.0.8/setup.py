import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fec-reader",
    version="1.0.8",
    author="Alexus Wong",
    author_email="alexus888@gmail.com",
    description="retrieves data from FEC.gov website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexus888/fec-reader",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'pandas', 'lxml', 'html5lib', 'BeautifulSoup4',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
