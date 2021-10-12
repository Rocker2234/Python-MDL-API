from setuptools import setup


# Use README for the PyPI page
with open('README.md') as f:
    long_description = f.read()

setup(
    name='mdl-scraper',
    version='0.0.1',
    license='MIT',
    description='Web Scraping API to fetch data from MDL',
    url='https://github.com/Rocker2234/Python-MDL-API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['PyMDL'],
    install_requires=['beautifulsoup4', 'requests'],
    keywords='MDL movie api MyDramaList'
)
