from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='craft-api',
    version='0.1.0',
    autor='The Pycraft Team @ SNUGifted \'18',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/minecraft-codingmath/pycraft-api',
    packages=find_packages(),
    install_requires=[
        'msgpack_python==0.5.6',
        'pyzmq==17.1.2'
    ],
    project_urls={
        'Source': 'https://github.com/minecraft-codingmath/pycraft-api',
        'Bug Reports': 'https://github.com/minecraft-codingmath/pycraft-api/issues'
    }
)
