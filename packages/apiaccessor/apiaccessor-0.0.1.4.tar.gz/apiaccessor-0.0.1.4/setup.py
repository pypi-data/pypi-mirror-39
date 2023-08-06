import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='apiaccessor',
    version='0.0.1.4',
    author='Daniel Cai',
    author_email='',
    description='A module to access API\'s using OAuth2 or Header-Key authentication.',
    long_description=long_description,
    # long_description_content_type='text/markdown',
    url='https://github.com/MrTrainCow/API-Accessor',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
