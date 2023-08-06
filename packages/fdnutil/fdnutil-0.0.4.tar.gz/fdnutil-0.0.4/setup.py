import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fdnutil",
    version="0.0.4",
    author="Ykäz Mihar",
    author_email="zaky@femaledaily.com",
    description="FDN Common utilities",
    long_description=long_description,
    install_requires=[
        'tinydb','python-telegram-bot'
    ],
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
)