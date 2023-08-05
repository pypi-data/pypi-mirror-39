import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_html_table",
    version="0.0.6",
    author="Harinath Selvaraj",
    author_email="harinath.selvaraj@outlook.com",
    description="Python library to extract data from HTML Tables with rowspan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harinathselvaraj/py_html_table",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
