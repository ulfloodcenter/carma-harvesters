import setuptools

long_description = 'CARMA data harvesters'

setuptools.setup(
    name="carma-harvesters",
    version="0.0.1",
    author="Brian Miles",
    author_email="brian.miles@louisiana.edu",
    description="CARMA harvester for HUC12 data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/watershedfloodcenter/carma-harvesters/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
    ],
    tests_require=[
    ],
    entry_points={
        'console_scripts': [
            'carma-huc12-extract=carma_harvesters.cmd.extract_huc12_definitions:main',
    ]},
)
