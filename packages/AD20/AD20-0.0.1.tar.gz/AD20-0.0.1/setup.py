import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AD20",
    version="0.0.1",
    author="Lindsey Brown, Xinyue Wang, Kevin Yoon",
    author_email=" ",
    description="Automatic Differentiation package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CS207-AD20/cs207-FinalProject",
    packages=setuptools.find_packages(),
    install_requires=['numpy==1.15.2',
                      'pandas==0.23.4',
                      'networkx==2.2',
                      'matplotlib==3.0.2',
                      'pandastable==0.11.0',
                      'scipy==1.1.0',
                      'pytest-timeout==1.2.1',
                      'pytest==3.4.2', 
                      'pytest-cov==2.5.1',
                      'pytest-dependency==0.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)