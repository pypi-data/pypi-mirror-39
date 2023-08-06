import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="qlikEngineConnect",
    version="1.0.0",
    description="Web-socket connector for Qlik engine API. ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/PalashPandey/qlik-engine-api-connector/",
    author="Palash Pandey",
    author_email="pp535@drexel.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=['qlikEngine'],
    include_package_data=True,
    install_requires=["websocket", "requests"]
)