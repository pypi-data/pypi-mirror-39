"""Package metadata for PyPI."""
from setuptools import setup


setup(
    name="scripted",
    version="0.0.0",
    description="MVC framework for CLI applications.",
    url="http://github.com/infosmith/scripted",
    author="infosmith",
    author_email="infosmith@protonmail.com",
    license="MIT",
    packages=["scripted", "scripted.core"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
