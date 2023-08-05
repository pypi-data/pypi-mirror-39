from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="xontrib-rerun",
    version="0.11",
    url="https://github.com/kmarilleau/xontrib-rerun",
    license="GPLv3+",
    classifiers=[
        "Environment :: Console",
        "Environment :: Plugins",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    author="Kevin Marilleau",
    author_email="kevin.marilleau@gmail.com",
    description="Rerun previous commands",
    long_description=long_description,
    install_requires=["docopt", "mdv", "psutil", "schema", "xonsh"],
    packages=["xontrib"],
    package_dir={"xontrib": "xontrib"},
    package_data={"xontrib": ["*.xsh"]},
    platforms="any",
)