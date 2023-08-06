import setuptools
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setuptools.setup(
    name="sorting_asmaa",
    version="0.0.8",
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
    long_description=long_description,

)
