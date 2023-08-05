import setuptools

setuptools.setup(
    name='libgeb',
    version='0.1.0',
    author='Antony B Holmes',
    author_email='antony.b.holmes@gmail.com',
    description='A library for reading and writing binary genomic element files.',
    url='https://github.com/antonybholmes/libgeb',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
