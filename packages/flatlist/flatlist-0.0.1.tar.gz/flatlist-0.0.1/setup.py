import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='flatlist',
    version='0.0.1',
    author='MJ Krakowski',
    author_email='mjk@c40.pl',
    description='Recursively flattens a list of any depth. '
                'Made just to check pypi and travis ;)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dwabece/flatlist',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: Public Domain',
        'Operating System :: OS Independent',
    ],
)
