import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="sesd",
    version="0.1.0",
    author="Nacho Navarro",
    author_email="nachonavarroasv@gmail.com",
    description="Anomaly detection algorithm implemented at Twitter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["sesd"],
    url="https://github.com/nachonavarro/seasonal-esd-anomaly-detection",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)