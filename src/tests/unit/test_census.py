import unittest
import os

from carma_harvesters.census import get_county_population


class TestCensus(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ.get('CENSUS_API_KEY')

    def test_get_county_population_single(self):
        # Test fetching most recent population estimate
        population_est = get_county_population(self.api_key,
                                                2019, '22', '055')
        self.assertEqual(1, len(population_est))
        d = population_est[0]
        self.assertEqual('Lafayette Parish, Louisiana', d.name)
        self.assertEqual('22', d.state_fips)
        self.assertEqual('055', d.county_fips)
        self.assertIsNotNone(d.last_update)
        self.assertEqual(2019, d.year)
        self.assertEqual(244390, d.population)

        # Testing fetching 2010 decennial
        population = get_county_population(self.api_key,
                                           2010, '22', '055')
        self.assertEqual(1, len(population))
        d = population[0]
        self.assertEqual('Lafayette Parish, Louisiana', d.name)
        self.assertEqual('22', d.state_fips)
        self.assertEqual('055', d.county_fips)
        self.assertEqual(2010, d.year)
        self.assertEqual(221578, d.population)

    def test_get_county_population_multiple(self):
        # Test fetching most recent population estimate
        population_est = get_county_population(self.api_key,
                                               2019, '22')
        self.assertEqual(64, len(population_est))
        # Test first element
        d = population_est[0]
        self.assertEqual('Richland Parish, Louisiana', d.name)
        self.assertEqual('22', d.state_fips)
        self.assertEqual('083', d.county_fips)
        self.assertIsNotNone(d.last_update)
        self.assertEqual(2019, d.year)
        self.assertEqual(20122, d.population)
        # Test last element
        d = population_est[-1]
        self.assertEqual('Concordia Parish, Louisiana', d.name)
        self.assertEqual('22', d.state_fips)
        self.assertEqual('029', d.county_fips)
        self.assertIsNotNone(d.last_update)
        self.assertEqual(2019, d.year)
        self.assertEqual(19259, d.population)


if __name__ == '__main__':
    unittest.main()
