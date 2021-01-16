import collections
from urllib.parse import urlparse

from carma_harvesters.geoconnex import Entity

ShortIDComponents = collections.namedtuple('ShortIDComponents', ['state_fips', 'county_fips'])


class County(Entity):
    @classmethod
    def generate_fq_id(cls, short_id: str) -> str:
        """
        Generate Internet of Water county IDs.
        `Example IDs <https://github.com/internetofwater/geoconnex.us/tree/master/namespaces/ref/counties>`_
        :param short_id: Short ID in the form of a county FIPS code, e.g. 08031.
        :return: Fully qualified county ID, e.g. https://geoconnex.us/ref/counties/08031
        """
        return f"https://geoconnex.us/ref/counties/{short_id}"

    @classmethod
    def parse_fq_id(cls, fq_id: str) -> ShortIDComponents:
        short_id = urlparse(fq_id).path.split('/')[-1]
        return ShortIDComponents(state_fips=short_id[:2], county_fips=short_id[2:])