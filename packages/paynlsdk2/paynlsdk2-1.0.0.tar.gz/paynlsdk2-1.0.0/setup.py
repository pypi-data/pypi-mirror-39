import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="paynlsdk2",
    version="1.0.0",
    author="Ing. R.J. van Dongen",
    author_email="rogier@sebsoft.nl",
    description="PayNL2 SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paynl/python2-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='PAYNL2, SDK, Python2',
    # Dependencies
    install_requires=[
        'marshmallow>=2,<3',
        'requests',
        'typing'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/paynl/python2-sdk/issues',
        'Source': 'https://github.com/paynl/python2-sdk/',
    },
)