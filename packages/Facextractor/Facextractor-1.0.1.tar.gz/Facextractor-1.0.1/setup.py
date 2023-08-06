from setuptools import setup


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name='Facextractor',
    version='1.0.1',
    description='Facebook Data Extractor, simple tool for read and analyze facebook dump (JSON format)',
    author='Jakub Janeček',
    author_email='jakub.janecek@fw-fw.cz',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/geekmoss/facextractor',
    install_requires=['Click'],
    scripts=['scripts/facextractor'],
    packages=['facextractor'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)