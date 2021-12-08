from setuptools import setup


# Use README for the PyPI page
with open('README.md') as f:
    long_description = f.read()

setup(
    name='PyMDL',
    version='0.1.0',
    license='MIT',
    description='Web Scraping API to fetch data from MDL',
    url='https://github.com/Rocker2234/Python-MDL-API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['PyMDL'],
    install_requires=['beautifulsoup4', 'requests', 'lxml'],
    keywords='MDL movie api MyDramaList',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search"
    ]
)
