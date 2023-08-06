import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="campy package",
    version="0.0.3",
    author="Kris Kurtin",
    author_email="kriskurtin@gmail.com",
    description="Class to grab frames from Basler cameras",
    long_description=long_description,
    long_description_content_type="",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
