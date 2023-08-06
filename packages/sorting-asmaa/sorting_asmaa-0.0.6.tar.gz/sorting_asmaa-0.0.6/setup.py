import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    long_description="""# Markdown supported!\n\n* Cheer\n* Celebrate\n""",
    long_description_content_type='text/markdown',
    name="sorting_asmaa",
    version="0.0.6",
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
