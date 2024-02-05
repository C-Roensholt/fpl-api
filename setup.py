from setuptools import setup

setup(
    name="fplapi",
    version="0.0.4",
    description="API wrapper for FPL",
    author="Christian Rønsholt",
    author_email="ronsholt32@gmail.com",
    license="MIT",
    python_requires=">=3.7",
    install_requires=open("requirements.txt").readlines(),
    long_description=open("README.md").read(),
    package_dir={"fplapi": "fplapi"},
    packages=["fplapi"],
)
