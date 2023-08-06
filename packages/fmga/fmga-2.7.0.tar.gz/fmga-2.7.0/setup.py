import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fmga',
    version='2.7.0',
    description='Genetic algorithms for n-dimensional function maximization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ameya Daigavane',
    author_email='ameya.d.98@gmail.com',
    url='https://github.com/ameya98/GeneticAlgorithmsRepo/tree/master/fmga',
    packages=setuptools.find_packages(),
    keywords=['genetic', 'genetic_algorithms'],
    install_requires=['numpy', 'pathos>=0.2.2.1'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
