import setuptools

long_description = 'CARMA data harvesters'

setuptools.setup(
    name="carma-harvesters",
    version="0.2.0",
    author="Brian Miles",
    author_email="brian.miles@louisiana.edu",
    description="CARMA harvesters for HUC12, county, & water user data",
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
            'carma-county-extract=carma_harvesters.cmd.extract_county_definitions:main',
            'carma-download-nwis-wateruse=carma_harvesters.cmd.download_nwis_water_use:main',
            'carma-subhuc12-generate=carma_harvesters.cmd.generate_subhuc12_definitions:main',
            'carma-groundwater-well-import=carma_harvesters.cmd.import_groundwater_wells:main',
            'carma-geojson-export=carma_harvesters.cmd.geojson_export:main',
            'carma-power-plant-wateruse-import=carma_harvesters.cmd.import_usgs_powerplant_wateruse:main',
            'carma-summarize-power-plant-wateruse=carma_harvesters.cmd.summarize_usgs_powerplant_wateruse:main',
            'carma-wassi-init=carma_harvesters.cmd.init_wassi_analysis:main',
            'carma-wassi-weight-generate=carma_harvesters.cmd.generate_wassi_weights:main'
    ]},
    include_package_data=True,
    zip_safe=False
)
