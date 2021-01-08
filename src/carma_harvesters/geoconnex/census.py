from carma_harvesters.geoconnex import Entity


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
