"""Setup."""
import io
from os import path
from setuptools import setup


here = path.abspath(path.dirname(__file__))

# io.open for py27
with io.open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# import __version__ attributes
about = {}
with open(path.join(here, "databricks_dbapi", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Database :: Front-Ends",
    ],
    keywords="databricks hive dbapi",
    packages=["databricks_dbapi"],
    install_requires=["pyhive[hive]"],
    include_package_data=False,
    zip_safe=False,
)
