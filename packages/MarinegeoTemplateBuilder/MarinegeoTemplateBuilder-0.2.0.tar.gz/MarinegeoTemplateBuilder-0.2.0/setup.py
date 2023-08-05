import setuptools

exec(open('MarinegeoTemplateBuilder/version.py').read())

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MarinegeoTemplateBuilder",
    version=__version__,
    author="Andy Bell",
    author_email="bellan@si.edu",
    description="Constructs MarineGEO data entry excel workbooks with built in validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MarineGEO/MarineGEO-template-builder",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'xlsxwriter',
        'pandas',
        'chardet',
        'xlrd',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)