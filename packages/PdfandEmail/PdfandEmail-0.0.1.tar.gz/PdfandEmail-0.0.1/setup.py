from setuptools import setup

with open('README.md', 'r') as ld:
    long_description = ld.read()

setup(
    author = "Apekshya Rimal",
    name='PdfandEmail',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Any format to pdf converter and Attach PDF in email",
    py_modules=["PdfandEmail"],
    package_dir={"": 'src'},
    classifiers=["Programming Language :: Python :: 3.0", "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8"]
)

