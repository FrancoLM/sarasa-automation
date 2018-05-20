from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='slayer',
    version='0.1.0a3',

    description='Slayer... the QA Automation Framework that came to SLAY!',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    url='https://github.com/FrancoLM/slayer',
    author='Franco Martinez',
    author_email='martinez.franco.leonardo@gmail.com',

    classifiers=[
        # How mature is this project?
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',

        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
    license="BSD",
    keywords='slayer automation framework',  # Optional
    install_requires=[
        "behave >= 1.2.6",
        "certifi >= 2018.4.16",
        "chardet >= 3.0.4",
        "configobj >= 5.0.6",
        "future >= 0.16.0",
        "idna >= 2.6",
        "parse >= 1.8.2",
        "parse-type >= 0.4.2",
        "PyYAML >= 3.12",
        "requests >= 2.18.4",
        "selenium >= 3.11.0",
        "six >= 1.11.0",
        "urllib3 >= 1.22",
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'output', 'deployment', 'tutorial']),  # Required
    include_package_data=True,
)
