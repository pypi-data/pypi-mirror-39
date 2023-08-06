from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name="sorting_asmaa",
    version="0.1.1",
    author="Asmaa Aly",
    author_email="asmaa.ali@minerva.kgi.edu",
    description="A sorting  package",
    url="https://github.com/asmaaalaa99/sorting",
    packages= ['sorting_asmaa'],
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    

)
