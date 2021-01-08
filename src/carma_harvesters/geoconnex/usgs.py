from carma_harvesters.geoconnex import Entity


class HydrologicUnit(Entity):
    @classmethod
    def generate_fq_id(cls, short_id: str) -> str:
        """
        Generate Internet of Water hydrologic unit IDs.
        `Example IDs <https://github.com/internetofwater/geoconnex.us/tree/master/namespaces/usgs>`_
        :param short_id: Short ID in the form of a HUC code, e.g. 07070005.
        :return: Fully qualified hydrologic unit ID, e.g. https://geoconnex.us/usgs/hydrologic-unit/07070005
        """
        return f"https://geoconnex.us/usgs/hydrologic-unit/{short_id}"
