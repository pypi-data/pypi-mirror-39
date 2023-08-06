import pathlib
from setuptools import setup

PROJECT_NAME = "PyQuantum"
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name=PROJECT_NAME,
    version="1.0.6",
    description="Python3 module for Quantum Mechanics",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexfmsu/"+PROJECT_NAME,
    author="alexfmsu",
    author_email="alexfmsu@mail.ru",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[PROJECT_NAME],
    include_package_data=True,
    install_requires=["numpy", "scipy", "pandas",
                      "matplotlib", "webbrowser", "html", "csv", "plotly", "importlib"],
    entry_points={
        "console_scripts": [
            PROJECT_NAME+"="+PROJECT_NAME+".__main__:main",
        ]
    },
)
