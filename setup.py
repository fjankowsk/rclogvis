import os.path
from setuptools import find_packages, setup


def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "rclogvis", "version.py")

    with open(version_file, "r") as f:
        raw = f.read()

    items = {}
    exec(raw, None, items)

    return items["__version__"]


def get_long_description():
    with open("README.md", "r") as fd:
        long_description = fd.read()

    return long_description


setup(
    name="rclogvis",
    version=get_version(),
    author="Fabian Jankowski",
    author_email="fjankowsk@gmail.com",
    description="Log visualisation for EdgeTX radios.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/fjankowsk/rclogvis",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "rclogvis-plot = rclogvis.apps.plot_data:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
)
