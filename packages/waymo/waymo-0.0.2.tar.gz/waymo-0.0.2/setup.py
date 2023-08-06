import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="waymo",
    version="0.0.2",
    author="cc189",
    author_email="cc189dev@gmail.com",
    description="Waymo pip package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GooglexTeam/waymo-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
