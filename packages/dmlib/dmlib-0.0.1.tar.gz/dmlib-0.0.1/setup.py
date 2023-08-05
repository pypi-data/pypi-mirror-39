import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='dmlib',
    version='0.0.1',
    author='Dmytro Brykovets',
    author_email='dmytro.brykovets@gmail.com',
    description='Math and statistics tools for data mining, linear programming etc.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/ortymid/dmlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
