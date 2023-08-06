import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getuipy",
    version="0.0.1",
    author="Samuel Lee",
    author_email="samuelx082@gmail.com",
    description="Not an official Getui SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lbhsot/getuipy.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)