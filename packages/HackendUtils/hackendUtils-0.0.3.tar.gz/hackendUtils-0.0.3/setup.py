import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hackendUtils",
    version="0.0.3",
    author="Hackend",
    author_email="office@hackend.org",
    description="utils for face recognition project",
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