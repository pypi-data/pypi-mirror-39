from .exceptions import UpdateError, APIException

EVENT_TYPES = {
    'CC': 'Chatbot Command',
}


class Event:
    def __init__(self, client, *args, **kwargs):
        self.client = client

        self.id = kwargs.get('id', None)
        self.event_type = kwargs.get('event_type', '')
        self.event_data = kwargs.get('event_data', '')
        self.active = kwargs.get('active', True)
        self.response_url = kwargs.get('response_url', '')

        dcta_id = kwargs['dcta']
        self.dcta = self.client.dctas[dcta_id]

    def __repr__(self):
        return '<Event: {}>'.format(self)

    def __str__(self):
        return '{}: {} ({})'.format(
            self.dcta.name, self.event_data, self.event_type
        )

    @classmethod
    def deserialize(cls, client, event_data={}):
        """
        Deserializes Event data from dictionary
        """
        return cls(client, **event_data)

    def serialize(self):
        """
        Serializes Event data to dictionary
        """
        data = {
            'id': self.id,
            'dcta': self.dcta.id,
            'active': self.active,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'response_url': self.response_url,
        }

        return data

    def update(self, **kwargs):
        """
        Updates an Event's information on the server and (if successful
        locally.
        """
        try:
            updated_data = self.client.patch('dcta-events/{}/'.format(self.id), kwargs)
        except APIException as error:
            raise UpdateError(
                'Could not update event: {}'.format(error.message)
            )

        # remove dcta so the link remains to the actual dcta object
        updated_data.pop('dcta', '')

        for key, value in updated_data.items():
            setattr(self, key, value)

        return self

    def delete(self):
        """
        Deletes an Event from the server and removes it from the DCTA's
        event list (effectively deleting it locally)
        """
        try:
            self.client.delete('dcta-events/{}/'.format(self.id))
        except APIException as error:
            raise UpdateError(
                'Could not delete event: {}'.format(error.message)
            )

        self.dcta.events = [event for event in self.dcta.events if event.id != self.id]
