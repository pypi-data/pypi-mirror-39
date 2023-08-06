from unittest import TestCase
from unittest.mock import patch

import responses

from adv.client import AdvClient
from adv.events import Event
from adv.dctas import DCTA


class EventTests(TestCase):
    def setUp(self):
        self.client = AdvClient('test-api-client')
        self.dcta = DCTA(self.client, id=15, name='Test DCTA')
        self.client.dctas[15] = self.dcta

    def test_basic_deserialization(self):
        """
        `deserialize` should create an Event object from the
        the dict
        """
        event_data = {
            'dcta': self.dcta.id,
            'id': 3,
            'event_type': 'CC',
            'event_data': 'answer Hearthstone',
            'response_url': 'https://my-response/url/',
            'active': True,
        }

        event = Event.deserialize(self.client, event_data)

        self.assertEqual(event.dcta, self.dcta)
        self.assertEqual(event.event_data, 'answer Hearthstone')
        self.assertEqual(event.response_url, 'https://my-response/url/')
        self.assertEqual(event.event_type, 'CC')

    def test_basic_serialization(self):
        """
        `serialize` should transform all relevant data into a dictionary
        """
        event = Event(
            self.client,
            id=3,
            dcta=self.dcta.id,
            event_type='CC',
            event_data='answer Hearthstone',
            response_url='https://my-response/url/',
        )

        expected_data = {
            'dcta': self.dcta.id,
            'id': 3,
            'event_type': 'CC',
            'event_data': 'answer Hearthstone',
            'response_url': 'https://my-response/url/',
            'active': True,
        }

        self.assertEqual(event.serialize(), expected_data)

    @patch('adv.client.AdvClient.delete')
    @responses.activate
    def test_delete_removes_event(self, mock_delete):
        """
        `Event.delete` should send a DELETE to the proper endpoint and,
        if successful, remove the event fromt he client
        """
        shared_response = {
            'dcta': self.dcta.id,
            'event_type': 'CC',
            'response_url': 'https://my-response/url/',
            'active': True,
        }

        event_1_response = {
            **shared_response,
            'event_data': 'answer Hearthstone',
            'id': 3,
        }

        event_2_response = {
            **shared_response,
            'event_data': 'answer Dota 2',
            'id': 4,
        }

        responses.add(
            responses.POST, 'https://api.adv.gg/v1/dcta-events/',
            json=event_1_response, status=201,
        )
        responses.add(
            responses.POST, 'https://api.adv.gg/v1/dcta-events/',
            json=event_2_response, status=201,
        )
        self.dcta.add_command_event(command='answer Hearthstone', response_url='https://my-response/url/')
        self.dcta.add_command_event(command='answer Dota 2', response_url='https://my-response/url/')

        self.assertEqual(len(self.dcta.events), 2)

        event = self.dcta.events[0]
        event.delete()

        self.assertEqual(len(self.dcta.events), 1)
