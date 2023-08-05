import unittest
import pandas as pd
import os
import logging
from dativa.tools.pandas.attribution_tools import Shapley
from pandas.util.testing import assert_frame_equal

logger = logging.getLogger("dativa.tools.attribution.tests")


class AttributionTest(unittest.TestCase):
    base_path = "{0}/test_data/attribution/".format(
        os.path.dirname(os.path.abspath(__file__)))

    def test_shapley(self):

        df_campaigns = pd.read_csv(self.base_path + 'impressions.csv')
        df_conversions = pd.read_csv(self.base_path + 'conversions.csv')

        s = Shapley(df_campaigns, df_conversions, 'viewer_id', 'campaign_id')

        results = s.run()
        expected = pd.DataFrame([['A', 0.29924242],
                                 ['C', 0.03787878],
                                 ['B', -0.33712121]],
                                columns=['campaign_id', 'Shapley_val'])
        assert_frame_equal(results, expected, check_exact=False)

    def test_shapley_invalid_default(self):

        df_campaigns = pd.read_csv(self.base_path + 'impressions.csv')
        df_conversions = pd.read_csv(self.base_path + 'conversions.csv')

        with self.assertRaises(TypeError):
            s = Shapley(df_campaigns, df_conversions, 'viewer_id', 'campaign_id', default_score='error')

    def test_shapley_duplicate_columns(self):

        df_campaigns = pd.read_csv(self.base_path + 'impressions.csv').rename(columns={'campaign_id': 'marker'})
        df_conversions = pd.read_csv(self.base_path + 'conversions.csv')
        s = Shapley(df_campaigns, df_conversions, 'viewer_id', 'marker')
        results = s.run()
        expected = pd.DataFrame([['A', 0.29924242],
                                 ['C', 0.03787878],
                                 ['B', -0.33712121]],
                                columns=['marker', 'Shapley_val'])
        assert_frame_equal(results, expected, check_exact=False)

    def test_shapley_colon_in_sets(self):

        df_campaigns = pd.read_csv(self.base_path + 'impressions.csv')
        df_conversions = pd.read_csv(self.base_path + 'conversions.csv')

        df_campaigns['campaign_id'] = df_campaigns['campaign_id'].str.replace('A', 'A:')

        s = Shapley(df_campaigns, df_conversions, 'viewer_id', 'campaign_id')
        results = s.run()
        expected = pd.DataFrame([['A:', 0.29924242],
                                 ['C', 0.03787878],
                                 ['B', -0.33712121]],
                                columns=['campaign_id', 'Shapley_val'])
        assert_frame_equal(results, expected, check_exact=False)