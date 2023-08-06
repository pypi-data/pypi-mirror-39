import setuptools

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="prezzibenzina_py",
    version="1.1.4",
    author="Eliseo Martelli",
    author_email="me@eliseomartelli.it",
    description="A python package to get Prezzibenzina info",
    long_description=long_description,
    url="https://github.com/eliseomartelli/prezzibenzina_py",
    packages=setuptools.find_packages(),
    install_requires=list(val.strip() for val in open('requirements.txt')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)