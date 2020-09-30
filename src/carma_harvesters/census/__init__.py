
# Census API query examples:
# https://api.census.gov/data/2019/pep/population?get=NAME,POP,LASTUPDATE&for=county:055&in=state:22
# https://api.census.gov/data/2017/pep/population?get=GEONAME,POP,LASTUPDATE&for=county:055&in=state:22
# https://api.census.gov/data/2015/pep/population?get=GEONAME,POP,LASTUPDATE&for=county:055&in=state:22
# https://api.census.gov/data/2010/dec/sf2?get=NAME,PCT001001&for=county:055&in=state:22
#
# API documentation: https://api.census.gov/data.html
#
# Consider using census package: https://pypi.org/project/census/
# Otherwise make direct calls using requests, etc.
#


def get_county_population(stco_fipscode, year):
    pass
