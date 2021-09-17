# Copyright (C) 2021-present University of Louisiana at Lafayette.
# All rights reserved. Licensed under the GPLv3 License. See LICENSE.txt in the project root for license information.

import unittest

from carma_harvesters.analysis.conversion import *

class TestConversions(unittest.TestCase):
    def test_cfs_to_mgd(self):
        value_mgd = cfs_to_mgd(20.489)
        self.assertAlmostEqual(13.2424283, value_mgd)

    def test_mm_per_km2_per_yr_to_mgd(self):
        value_mgd = mm_per_km2_per_yr_to_mgd(160.67391304347825,
                                             57.4878743558)
        self.assertAlmostEqual(6.680643, value_mgd)

    def test_cfs_to_acre_ft_per_yr(self):
        value_acre_ft_yr = cfs_to_acre_ft_per_yr(154.94)
        self.assertAlmostEqual(112245.961258, value_acre_ft_yr, places=4)

    def test_mm_per_km2_per_yr_to_acre_ft_per_yr(self):
        value_acre_ft_yr = mm_per_km2_per_yr_to_acre_ft_per_year(160.67391304347825,
                                                                 57.4878743558)
        self.assertAlmostEqual(7488.2432180838, value_acre_ft_yr, places=4)