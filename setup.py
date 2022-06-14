import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()
requires = [
    "pymongo>=3.0"
]
setuptools.setup(
    name = "dgrpy_mongodb",
    version = "0.0.9",
    author = "donugr",
    author_email = "donugr@hotmail.com",
    description = "mongodb module in python 3",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/donugr/dgrpy_mongodb",
    install_requires=requires,
    include_package_data=True,
    project_urls = {
        "Bug Tracker": "https://github.com/donugr/dgrpy_mongodb",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)