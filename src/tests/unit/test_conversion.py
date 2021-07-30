import unittest

from carma_harvesters.analysis.conversion import cfs_to_mgd, mm_per_km2_per_yr_to_mgd

class TestConversions(unittest.TestCase):
    def test_cfs_to_mgd(self):
        value_mgd = cfs_to_mgd(20.489)
        self.assertAlmostEqual(13.2424283, value_mgd)

    def test_mm_per_km2_per_yr_to_mgd(self):
        value_mgd = mm_per_km2_per_yr_to_mgd(160.67391304347825,
                                             57.4878743558)
        self.assertAlmostEqual(6.680643, value_mgd)
