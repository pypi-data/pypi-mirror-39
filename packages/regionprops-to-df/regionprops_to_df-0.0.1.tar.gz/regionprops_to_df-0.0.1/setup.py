import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'regionprops_to_df',
    version = '0.0.1',
    description = 'Converts output of skimage.measure.regionprops to Pandas df',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Chigozie Nri',
    author_email = 'chigozie@gmail.com',
    url = 'https://github.com/chigozienri/regionprops_to_df',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
)
