from .dctas import DCTA
from .exceptions import UpdateError, APIException


class Campaign:
    def __init__(self, client, name, slug):
        self.client = client
        self.name = name
        self.slug = slug

    def create_dcta(self, **kwargs):
        """
        Creates a new DCTA on this campaign
        """
        try:
            dcta_data = self.client.post('dctas/', {'campaign': self.slug, **kwargs})
        except APIException as error:
            raise UpdateError(
                'Could not create new DCTA on campaign {}: {}'.format(self.name, error.message)
            )

        dcta = DCTA.deserialize(self.client, dcta_data)

        return dcta

    def __repr__(self):
        return '<Campaign: {}>'.format(self)

    def __str__(self):
        return self.name
