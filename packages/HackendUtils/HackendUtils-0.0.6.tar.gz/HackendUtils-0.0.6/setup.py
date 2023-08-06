import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HackendUtils",
    version="0.0.6",
    author="Hackend",
    author_email="office@hackend.org",
    description="utils for hackend's python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hackendOrg/HackendPython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)