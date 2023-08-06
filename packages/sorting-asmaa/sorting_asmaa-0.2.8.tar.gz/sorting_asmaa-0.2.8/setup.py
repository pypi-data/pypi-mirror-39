import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="sorting_asmaa",
    version="0.2.8",
    author="Asmaa Aly",
    author_email="asmaa.ali@minerva.kgi.edu",
    description="A sorting  package",
    url="https://github.com/asmaaalaa99/sorting",
    packages= ['sorting_asmaa'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    

)
