
SECTORS = ["Public Supply",
           "Domestic",
           "Commercial",
           "Industrial",
           "Total Thermoelectric Power",
           "Fossil-fuel Thermoelectric Power",
           "Geothermal Thermoelectric Power",
           "Nuclear Thermoelectric Power",
           "Thermoelectric Power (Once-through cooling)",
           "Thermoelectric Power (Closed-loop cooling)",
           "Mining",
           "Livestock",
           "Livestock (Stock)",
           "Livestock (Animal Specialities)",
           "Aquaculture",
           "Irrigation",
           "Irrigation, Sprinkler"
           "Irrigation, Crop",
           "Irrigation, Microirrigation"
           "Irrigation, Golf Courses",
           "Hydroelectric Power",
           "Wastewater Treatment"]

POPULATION_CATEGORY = 'Total Population total population of area, in thousands'

# TODO: Make descriptors objects instead of dicts so that they can be hashed to
# determine uniqueness and to support sorting
CATEGORY_DESCRIPTORS = {
    "Public Supply population served by groundwater, in thousands":
        {
            "sector": "Public Supply",
            "entity_type": "Person",
            "water_source": "Groundwater",
            "water_type": "N/A",
            "description": "Public Supply population served by groundwater, in thousands",
            "unit": {"name": "thousand",
                     "primaryDimension": "Thousand"}
        },
    "Public Supply population served by surface water, in thousands":
        {
            "sector": "Public Supply",
            "entity_type": "Person",
            "water_source": "Surface Water",
            "water_type": "N/A",
            "description": "Public Supply population served by surface water, in thousands",
            "unit": {"name": "thousand",
                     "primaryDimension": "Thousand"}
        },
    "Public Supply total population served, in thousands":
        {
            "sector": "Public Supply",
            "entity_type": "Person",
            "water_source": "All",
            "water_type": "N/A",
            "description": "Public Supply total population served, in thousands",
            "unit": {"name": "thousand",
                     "primaryDimension": "Thousand"}
        },
    "Public Supply self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Public Supply self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
         },
    "Public Supply self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Public Supply self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Public Supply total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Public Supply self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Public Supply self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Public Supply total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Public Supply total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Public Supply total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply total self-supplied withdrawals, total, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply total self-supplied withdrawals, total, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply deliveries to domestic, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply deliveries to domestic, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply deliveries to commercial, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply deliveries to commercial, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply deliveries to industrial, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply deliveries to industrial, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply deliveries to thermoelectric, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply deliveries to thermoelectric, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply total deliveries, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply total deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply public use and losses, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply public use and losses, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply per capita use, in gallons/person/day":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Public Supply per capita use, in gallons/person/day",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Gallon",
                     "secondaryDimension": "Capita",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply reclaimed wastewater, in Mgal/d":
        {
            "sector": "Public Supply",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Public Supply reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Public Supply number of facilities":
        {
            "sector": "Public Supply",
            "entity_type": "Facility",
            "water_source": "All",
            "water_type": "N/A",
            "description": "Public Supply number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Domestic self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Domestic self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Domestic self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Domestic total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Domestic self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Domestic self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Domestic total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic self-supplied population, in thousands":
        {
            "sector": "Domestic",
            "entity_type": "Person",
            "water_source": "All",
            "water_type": "N/A",
            "description": "Domestic self-supplied population, in thousands",
            "unit": {"name": "",
                     "primaryDimension": "Thousand"}
        },
    "Domestic deliveries from public supply, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Domestic total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic per capita use, public-supplied, in gallons/person/day":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic per capita use, public-supplied, in gallons/person/day",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Gallon",
                     "secondaryDimension": "Capita",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic consumptive use, fresh, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Domestic consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic consumptive use, saline, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Domestic consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic total consumptive use, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Domestic per capita use, self-supplied, in gallons/person/day":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Domestic per capita use, self-supplied, in gallons/person/day",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Gallon",
                     "secondaryDimension": "Capita",
                     "tertiaryDimension": "Day"}
        },
    "Domestic reclaimed wastewater, in Mgal/d":
        {
            "sector": "Domestic",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Domestic reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Commercial self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Commercial self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Commercial total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Commercial self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Commercial self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Commercial total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Commercial total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Commercial total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Commercial total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial deliveries from public supply, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Commercial deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Commercial total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial consumptive use, fresh, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Commercial consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial consumptive use, saline, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Commercial consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial total consumptive use, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Commercial total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Commercial reclaimed wastewater, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Commercial reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Industrial self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Industrial self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Industrial total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Industrial self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Industrial self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Industrial total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Industrial total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Industrial total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Industrial total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial deliveries from public supply, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Industrial deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Industrial total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial consumptive use, fresh, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Industrial consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial consumptive use, saline, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Industrial consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial total consumptive use, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Industrial total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial reclaimed wastewater, in Mgal/d":
        {
            "sector": "Industrial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Industrial reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Industrial number of facilities":
        {
            "sector": "Industrial",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Industrial number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Total Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Total Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Total Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Total Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Total Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Total Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Total Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Total Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Total Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total self-supplied withdrawals, total, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Total Thermoelectric Power total self-supplied withdrawals, total, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Total Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power consumptive use, fresh, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Total Thermoelectric Power consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power consumptive use, saline, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Total Thermoelectric Power consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power total consumptive use, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Total Thermoelectric Power total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power power generated, in gigawatt-hours":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Total Thermoelectric Power power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Total Thermoelectric Power reclaimed wastewater, in Mgal/d":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Total Thermoelectric Power reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Total Thermoelectric Power number of facilities":
        {
            "sector": "Total Thermoelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Total Thermoelectric Power number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Fossil-fuel Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Fossil-fuel Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Fossil-fuel Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Fossil-fuel Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Fossil-fuel Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Fossil-fuel Thermoelectric Power total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power deliveries from public supply, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Fossil-fuel Thermoelectric Power deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Fossil-fuel Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power consumptive use, fresh, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Fossil-fuel Thermoelectric Power consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power consumptive use, saline, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Fossil-fuel Thermoelectric Power consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power total consumptive use, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Fossil-fuel Thermoelectric Power total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power power generation, in gigawatt-hours":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Fossil-fuel Thermoelectric Power power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Fossil-fuel Thermoelectric Power reclaimed wastewater, in Mgal/d":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Fossil-fuel Thermoelectric Power reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Fossil-fuel Thermoelectric Power number of facilities":
        {
            "sector": "Fossil-fuel Thermoelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Fossil-fuel Thermoelectric Power number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Geothermal Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Geothermal Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Geothermal Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Geothermal Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Geothermal Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Geothermal Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Geothermal Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Geothermal Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Geothermal Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Geothermal Thermoelectric Power total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power deliveries from public supply, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Geothermal Thermoelectric Power deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Geothermal Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power consumptive use, fresh, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Geothermal Thermoelectric Power consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power consumptive use, saline, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Geothermal Thermoelectric Power consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power total consumptive use, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Geothermal Thermoelectric Power total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power power generation, in gigawatt-hours":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Geothermal Thermoelectric Power power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Geothermal Thermoelectric Power reclaimed wastewater, in Mgal/d":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Geothermal Thermoelectric Power reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Geothermal Thermoelectric Power number of facilities":
        {
            "sector": "Geothermal Thermoelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Geothermal Thermoelectric Power number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Nuclear Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Nuclear Thermoelectric Power self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Nuclear Thermoelectric Power self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Nuclear Thermoelectric Power total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Nuclear Thermoelectric Power self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Nuclear Thermoelectric Power self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Nuclear Thermoelectric Power total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Nuclear Thermoelectric Power total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Nuclear Thermoelectric Power total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Nuclear Thermoelectric Power total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power deliveries from public supply, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Nuclear Thermoelectric Power deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Nuclear Thermoelectric Power total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power consumptive use, fresh, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Nuclear Thermoelectric Power consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power consumptive use, saline, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Nuclear Thermoelectric Power consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power total consumptive use, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Nuclear Thermoelectric Power total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power power generation, in gigawatt-hours":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Nuclear Thermoelectric Power power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Nuclear Thermoelectric Power reclaimed wastewater, in Mgal/d":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Nuclear Thermoelectric Power reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Nuclear Thermoelectric Power number of facilities":
        {
            "sector": "Nuclear Thermoelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Nuclear Thermoelectric Power number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Thermoelectric Power (Once-through cooling) self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Once-through cooling) self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Once-through cooling) self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) self-supplied surface-water withdrawals, fresh, in Mgal/":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Once-through cooling) self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) self-supplied surface-water withdrawals, saline, in Mgal":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Once-through cooling) self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, surface water, in Mgal/":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, total, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals, total, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) deliveries from public supply, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Once-through cooling) deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals plus deliveries, in Mgal":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Once-through cooling) total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) consumptive use, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Once-through cooling) consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) consumptive use, saline, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Once-through cooling) consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) total consumptive use, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Once-through cooling) total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) power generated, in gigawatt-hours":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Thermoelectric Power (Once-through cooling) power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Thermoelectric Power (Once-through cooling) reclaimed wastewater, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Thermoelectric Power (Once-through cooling) reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Once-through cooling) number of facilities":
        {
            "sector": "Thermoelectric Power (Once-through cooling)",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Thermoelectric Power (Once-through cooling) number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Thermoelectric Power (Closed-loop cooling) self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Closed-loop cooling) self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Closed-loop cooling) self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Closed-loop cooling) self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) self-supplied surface-water withdrawals, saline, in Mgal/":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Closed-loop cooling) self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, total, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals, total, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) deliveries from public supply, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Closed-loop cooling) deliveries from public supply, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals plus deliveries, in Mgal/":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Closed-loop cooling) total self-supplied withdrawals plus deliveries, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) consumptive use, fresh, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Thermoelectric Power (Closed-loop cooling) consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) consumptive use, saline, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Thermoelectric Power (Closed-loop cooling) consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) total consumptive use, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Thermoelectric Power (Closed-loop cooling) total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) power generated, in gigawatt-hours":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Thermoelectric Power (Closed-loop cooling) power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Thermoelectric Power (Closed-loop cooling) reclaimed wastewater, in Mgal/d":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Thermoelectric Power (Closed-loop cooling) reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Thermoelectric Power (Closed-loop cooling) number of facilities":
        {
            "sector": "Thermoelectric Power (Closed-loop cooling)",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Thermoelectric Power (Closed-loop cooling) number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Mining self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Mining self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Mining self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Mining total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Mining self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Mining self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Mining total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Mining total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Mining total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Mining total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining consumptive use, fresh, in Mgal/d":
        {
            "sector": "Commercial",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Mining consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining consumptive use, saline, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Mining consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining total consumptive use, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Mining total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Mining reclaimed wastewater, in Mgal/d":
        {
            "sector": "Mining",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Mining reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Livestock self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Livestock self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Livestock total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock consumptive use, fresh, in Mgal/d":
        {
            "sector": "Livestock",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Livestock consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Livestock (Stock) self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Livestock (Stock) self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Livestock (Stock) total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Livestock (Stock) self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Livestock (Stock) self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Livestock (Stock) total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Livestock (Stock) total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Livestock (Stock) total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Livestock (Stock) total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) consumptive use, fresh, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Livestock (Stock) consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) consumptive use, saline, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Livestock (Stock) consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Stock) total consumptive use, in Mgal/d":
        {
            "sector": "Livestock (Stock)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Livestock (Stock) total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Livestock (Animal Specialties) self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Livestock (Animal Specialties) self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Livestock (Animal Specialties) total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Livestock (Animal Specialties) self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Livestock (Animal Specialties) self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Livestock (Animal Specialties) total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Livestock (Animal Specialties) total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Livestock (Animal Specialties) total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Livestock (Animal Specialties) total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) consumptive use, fresh, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Livestock (Animal Specialties) consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) consumptive use, saline, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Livestock (Animal Specialties) consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Livestock (Animal Specialties) total consumptive use, in Mgal/d":
        {
            "sector": "Livestock (Animal Specialties)",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Livestock (Animal Specialties) total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Aquaculture self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Aquaculture self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Aquaculture total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Aquaculture self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Aquaculture self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Aquaculture total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Aquaculture total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Aquaculture total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Aquaculture total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture consumptive use, fresh, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Aquaculture consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture consumptive use, saline, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Aquaculture consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Aquaculture total consumptive use, in Mgal/d":
        {
            "sector": "Aquaculture",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Aquaculture total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total self-supplied groundwater withdrawals, fresh, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Irrigation, Total self-supplied groundwater withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total self-supplied groundwater withdrawals, saline, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Saline",
            "description": "Irrigation, Total self-supplied groundwater withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total total self-supplied withdrawals, groundwater, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Any",
            "description": "Irrigation, Total total self-supplied withdrawals, groundwater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total self-supplied surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Irrigation, Total self-supplied surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Wastewater Treatment reclaimed wastewater released by public wastewater facilities, in Mgal/d":
        {
            "sector": "Wastewater Treatment",
            "entity_type": "Water",
            "water_source": "Plant Discharge Water",
            "water_type": "Reclaimed",
            "description": "Wastewater Treatment reclaimed wastewater released by public wastewater facilities, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total self-supplied surface-water withdrawals, saline, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Irrigation, Total self-supplied surface-water withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total total self-supplied withdrawals, surface water, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Irrigation, Total total self-supplied withdrawals, surface water, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total total self-supplied withdrawals, fresh, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Irrigation, Total total self-supplied withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total total self-supplied withdrawals, saline, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Irrigation, Total total self-supplied withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total total self-supplied withdrawals, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Total total self-supplied withdrawals, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total consumptive use, fresh, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Irrigation, Total consumptive use, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total consumptive use, saline, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Saline",
            "description": "Irrigation, Total consumptive use, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total total consumptive use, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Total total consumptive use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total conveyance loss, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Total conveyance loss, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Total sprinkler irrigation, in thousand acres":
        {
            "sector": "Irrigation, Sprinkler",
            "entity_type": "Land",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Irrigation, Total sprinkler irrigation, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Total microirrigation, in thousand acres":
        {
            "sector": "Irrigation, Microirrigation",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Total microirrigation, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Total surface irrigation, in thousand acres":
        {
            "sector": "Irrigation",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Total surface irrigation, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Total total irrigation, in thousand acres":
        {
            "sector": "Irrigation",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Total total irrigation, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Total reclaimed wastewater, in Mgal/d":
        {
            "sector": "Irrigation",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Irrigation, Total reclaimed wastewater, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Crop self-supplied groundwater withdrawals for crops, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Irrigation, Crop self-supplied groundwater withdrawals for crops, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Crop self-supplied surface-water withdrawals for crops, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Irrigation, Crop self-supplied surface-water withdrawals for crops, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Crop total self-supplied withdrawals for crops, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Irrigation, Crop total self-supplied withdrawals for crops, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Crop consumptive use for crops, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Irrigation, Crop consumptive use for crops, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Crop conveyance loss for crops, in Mgal/d":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Crop conveyance loss for crops, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Crop sprinkler irrigation for crops, in thousand acres":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Crop sprinkler irrigation for crops, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Crop microirrigation for crops, in thousand acres":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Crop microirrigation for crops, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Crop surface irrigation for crops, in thousand acres":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Crop surface irrigation for crops, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Crop total irrigation for crops, in thousand acres":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Crop total irrigation for crops, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Crop reclaimed wastewater for crops, in Mgal/d":
        {
            "sector": "Irrigation, Crop",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Irrigation, Crop reclaimed wastewater for crops, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Golf Courses self-supplied groundwater withdrawals for golf courses, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Water",
            "water_source": "Groundwater",
            "water_type": "Fresh",
            "description": "Irrigation, Golf Courses self-supplied groundwater withdrawals for golf courses, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Golf Courses self-supplied surface-water withdrawals for golf courses, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Irrigation, Golf Courses self-supplied surface-water withdrawals for golf courses, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Golf Courses total self-supplied withdrawals for golf courses, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Irrigation, Golf Courses total self-supplied withdrawals for golf courses, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Golf Courses consumptive use for golf courses, fresh, in Mgal/d":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Fresh",
            "description": "Irrigation, Golf Courses consumptive use for golf courses, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Golf Courses conveyance loss for golf courses, in Mgal/d":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Golf Courses conveyance loss for golf courses, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Irrigation, Golf Courses sprinkler irrigation for golf courses, in thousand acres":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Golf Courses sprinkler irrigation for golf courses, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Golf Courses microirrigation for golf courses, in thousand acres":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Golf Courses microirrigation for golf courses, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Golf Courses surface irrigation for golf courses, in thousand acres":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Golf Courses surface irrigation for golf courses, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Golf Courses total irrigation for golf courses, in thousand acres":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Land",
            "water_source": "All",
            "water_type": "Any",
            "description": "Irrigation, Golf Courses total irrigation for golf courses, in thousand acres",
            "unit": {"name": "thousand acre",
                     "primaryDimension": "Thousand",
                     "secondaryDimension": "Acre"}
        },
    "Irrigation, Golf Courses reclaimed wastewater for golf courses, in Mgal/d":
        {
            "sector": "Irrigation, Golf Courses",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Irrigation, Golf Courses reclaimed wastewater for golf courses, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Hydroelectric Power instream water use, in Mgal/d":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Hydroelectric Power instream water use, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Hydroelectric Power offstream surface-water withdrawals, fresh, in Mgal/d":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Fresh",
            "description": "Hydroelectric Power offstream surface-water withdrawals, fresh, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Hydroelectric Power surface water self-supplied offstream withdrawals, saline, in Mgal/d":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Saline",
            "description": "Hydroelectric Power surface water self-supplied offstream withdrawals, saline, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Hydroelectric Power total offstream surface-water withdrawals in Mgal/d":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Hydroelectric Power total offstream surface-water withdrawals in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Hydroelectric Power power generated by instream use, in gigawatt-hours":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Hydroelectric Power power generated by instream use, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Hydroelectric Power power generated by offstream use, in gigawatt-hours":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Hydroelectric Power power generated by offstream use, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Hydroelectric Power total power generated, in gigawatt-hours":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Power",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Hydroelectric Power total power generated, in gigawatt-hours",
            "unit": {"name": "GWh", "primaryDimension": "Gigawatt",
                     "secondaryDimension": "Hour"}
        },
    "Hydroelectric Power number of instream facilities":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Hydroelectric Power number of instream facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Hydroelectric Power number of offstream facilities":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Hydroelectric Power number of offstream facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Hydroelectric Power total number of facilities":
        {
            "sector": "Hydroelectric Power",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Hydroelectric Power total number of facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Wastewater Treatment returns by public wastewater facilities, in Mgal/d":
        {
            "sector": "Wastewater Treatment",
            "entity_type": "Water",
            "water_source": "Surface Water",
            "water_type": "Any",
            "description": "Wastewater Treatment returns by public wastewater facilities, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        },
    "Wastewater Treatment number of public wastewater facilities":
        {
            "sector": "Wastewater Treatment",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Wastewater Treatment number of public wastewater facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Wastewater Treatment number of wastewater facilities":
        {
            "sector": "Wastewater Treatment",
            "entity_type": "Facility",
            "water_source": "N/A",
            "water_type": "N/A",
            "description": "Wastewater Treatment number of wastewater facilities",
            "unit": {"name": "",
                     "primaryDimension": "One"}
        },
    "Wastewater Treatment reclaimed wastewater released by wastewater facilities, in Mgal/d":
        {
            "sector": "Wastewater Treatment",
            "entity_type": "Water",
            "water_source": "All",
            "water_type": "Reclaimed",
            "description": "Wastewater Treatment reclaimed wastewater released by wastewater facilities, in Mgal/d",
            "unit": {"name": "Mgal/d",
                     "primaryDimension": "Million",
                     "secondaryDimension": "Gallon",
                     "tertiaryDimension": "Day"}
        }
}