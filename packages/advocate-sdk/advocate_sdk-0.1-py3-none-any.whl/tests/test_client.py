from unittest import TestCase
from unittest.mock import patch

from adv.client import AdvClient
from adv.exceptions import NoMatchException


class AdvClientTests(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = AdvClient('test-api-key')

    @patch('adv.client.AdvClient.get')
    def test_get_campaign(self, mock_get):
        """
        If a campaign exists in the user's campaigns, `get_campaign` should return the
        resulting `Campaign` object.  Otherwise, it should raise a `NoMatchException`.
        """
        campaign_data = [
            {
                'name': 'Test Campaign',
                'slug': 'test-campaign',
            },
            {
                'name': 'Other Campaign',
                'slug': 'other-campaign',
            },
        ]
        mock_get.return_value = campaign_data

        campaign = self.client.get_campaign('other-campaign')

        self.assertEqual(campaign.name, 'Other Campaign')
        self.assertEqual(campaign.slug, 'other-campaign')

        with self.assertRaises(NoMatchException) as error:
            campaign = self.client.get_campaign('wrong-campaign')

        self.assertEqual(
            error.exception.message,
            ('Campaign with slug value "wrong-campaign" either does not exist '
             'or cannot be accessed by this Advocate user.'),
        )
