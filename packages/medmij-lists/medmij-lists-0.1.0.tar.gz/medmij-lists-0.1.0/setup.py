from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='medmij-lists',
    install_requires=['lxml'],
    packages=['medmij_lists'],
    zip_safe=True,
    url='https://github.com/GidsOpenStandaarden/OpenPGO-Medmij-ImplementatieBouwstenen-Python',
    setup_requires=['nose'],
    test_suite='nose.collector',
    description='Python implementation of de MedMij ZAL, OCL, Whitelist and GNL',
    long_description=long_description,
    long_description_content_type="text/markdown",
    tests_require=['nose'],
    python_require=">=3.7",
    package_data={'medmij_lists': ['*.xsd']},
    version='0.1.0'
)
