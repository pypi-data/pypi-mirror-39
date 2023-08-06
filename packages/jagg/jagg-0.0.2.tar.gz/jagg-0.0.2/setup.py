from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='jagg',
    version='0.0.2',
    description='Judgment Aggregation',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='http://github.com/rdehaan/jagg',
    author='Ronald de Haan',
    author_email='me@ronalddehaan.eu',
    license='GPLv3',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
    ])
