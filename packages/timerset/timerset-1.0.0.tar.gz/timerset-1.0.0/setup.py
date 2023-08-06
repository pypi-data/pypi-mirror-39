import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timerset",
    version="1.0.0",
    author="Brendan Furey",
    author_email="brenpatf@gmail.com",
    description="Code timing class",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brenpatf/timerset",
    packages=["timerset", "timerset.examples.colgroup", "timerset.test", "timerset.test.timerset"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)