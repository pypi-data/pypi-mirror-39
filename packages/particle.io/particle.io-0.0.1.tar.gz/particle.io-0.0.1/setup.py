import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="particle.io",
    version="0.0.1",
    author="Weblabz LLC",
    author_email="lance@weblabz.io",
    description="SDK for the Particle.io API ",
    long_description=long_description,
    url="https://github.com/drankinn/particle.io",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ]
)
