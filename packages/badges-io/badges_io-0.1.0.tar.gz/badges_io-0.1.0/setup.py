from setuptools import setup

def read(fname):
    with open(fname) as f:
        return f.read()

setup(
    name='badges_io',
    packages=['badges_io'],
    version='0.1.0',
    description='Uploads total coverage for displaying badge',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[],
    author='Samuel Carlsson',
    author_email='samuel.carlsson@volumental.com',
    url='https://github.com/Volumental/badges',
    keywords=['badge', 'shield', 'shields.io'],
)
