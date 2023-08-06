import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sorting_asmaa",
    version="0.1.8",
    author="Asmaa Aly",
    author_email="asmaa.ali@minerva.kgi.edu",
    description="A sorting  package",
    url="https://github.com/asmaaalaa99/sorting",
    packages= ['sorting_asmaa'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    

)
