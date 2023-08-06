import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

build_major = 0
build_minor = os.getenv('CIRCLE_BUILD_NUM', '4')
build_number = f"{build_major}.{build_minor}"

setup(
    name='django-epsilon',
    version=build_number,
    description='Django Epsilon service',
    url='',
    author='',
    author_email='',
    license='MIT',
    packages=find_packages(exclude=["tests.*", "tests", "test*"]),
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'django',
        'schema'
    ],
    zip_safe=False
)
