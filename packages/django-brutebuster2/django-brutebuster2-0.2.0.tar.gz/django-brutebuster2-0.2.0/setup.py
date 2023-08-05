import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-brutebuster2",
    version="0.2.0",
    author="MTR Design",
    author_email="office@mtr-design.com",
    description="Django Bruteforce Buster",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtrdesign/django-brutebuster/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
