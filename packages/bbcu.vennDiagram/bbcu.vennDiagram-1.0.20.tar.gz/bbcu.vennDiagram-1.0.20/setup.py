from setuptools import setup, find_packages

with open('VERSION.txt', 'r') as version_file:
    version = version_file.read().strip()

requires = ['xlrd==1.1.0','pandas==0.23.4','scipy==1.1.0','matplotlib==2.2.3']


setup(
    name='bbcu.vennDiagram',
    version=version,
    author='Refael Kohen',
    author_email='refael.kohen@weizmann.ac.il',
    packages=find_packages(),
    scripts=[
        'scripts/create-venn.py',
    ],
    description='Create venn diagram from intersection between input files.',
    long_description=open('README.txt').read(),
    install_requires=requires,
    tests_require=requires + ['nose'],
    include_package_data=True,
    test_suite='nose.collector',
)
