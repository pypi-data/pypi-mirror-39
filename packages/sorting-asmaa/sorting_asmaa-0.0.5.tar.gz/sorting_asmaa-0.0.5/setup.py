import setuptools
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
setuptools.setup(
    name="sorting_asmaa",
    version="0.0.5",
    author="Asmaa Aly",
    author_email="asmaa.ali@minerva.kgi.edu",
    description="A sorting  package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asmaaalaa99/sorting",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
