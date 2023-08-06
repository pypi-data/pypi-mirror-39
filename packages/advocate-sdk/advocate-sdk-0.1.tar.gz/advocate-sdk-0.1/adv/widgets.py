import os

from .exceptions import UpdateError, APIException


class Widget:
    # List of dictionaries with the following keys:
    #    `name`: the name of the extra field on the widget
    #    `default` (optional): the value to use if there is none passed into init
    extra_fields = []

    def __init__(self, client, *args, **kwargs):
        self.client = client

        self.id = kwargs.get('id', None)
        self.parent = kwargs.get('parent', None)
        self.attributes = kwargs.get('attributes', {})
        self.styles = kwargs.get('styles', {})
        self.broadcasters = kwargs.get('broadcasters', [])
        self.name = kwargs.get('name', '')

        dcta_id = kwargs['dcta']
        self.dcta = self.client.dctas[dcta_id]

        for field in self.extra_fields:
            try:
                setattr(
                    self, field['name'], kwargs.get(field['name'], field.get('default', None))
                )
            except KeyError:
                raise ValueError(
                    'All items in `extra_fields` must be a dictionary with a `name` key'
                )

    @classmethod
    def deserialize(cls, client, widget_data={}):
        """
        Deserializes Widget data from dictionary
        """
        return cls(client, **widget_data)

    def serialize(self):
        """
        Serializes Widget data to dictionary
        """
        data = {
            'name': self.name,
            'parent': self.parent,
            'attributes': self.attributes,
            'styles': self.styles,
            'type': self.type,
            'broadcasters': [],
            'dcta': self.dcta.id,
            'id': self.id
        }

        for field in self.extra_fields:
            data[field['name']] = getattr(self, field['name'])

        return data

    def __repr__(self):
        return '<Widget ({}): {}>'.format(self.type, self.name)

    def __str__(self):
        return self.name

    @property
    def type(self):
        return self.__class__.__name__.replace('Widget', '').lower()

    def update(self, force_render=False, files=None, **kwargs):
        """
        Updates a widget's data on the server (and locally).  Use `force_render` to
        render the DCTA to all active browsersources when the update is done
        """
        new_data = {}

        for key, value in kwargs.items():
            new_data[key] = value

        try:
            updated_data = self.client.patch('widgets/{}/{}/'.format(self.type, self.id), new_data, files=files)
        except APIException as error:
            raise UpdateError(
                'Could not update widget: {}'.format(error.message)
            )

        # remove dcta so the link remains to the actual dcta object
        updated_data.pop('dcta', '')

        for key, value in updated_data.items():
            setattr(self, key, value)

        if force_render:
            self.dcta.render()

        return self

    def update_style(self, style_name, style_value, force_render=False):
        """
        Update a single style
        """
        new_styles = {
            **self.styles,
            style_name: style_value,
        }

        self.update(styles=new_styles, force_render=force_render)


class TextWidget(Widget):
    extra_fields = [{'name': 'text', 'default': ''}]
    type = 'text'


class ImageWidget(Widget):
    extra_fields = [{'name': 'src'}]
    type = 'image'

    def update(self, force_render=False, files=None, **kwargs):
        src = kwargs.pop('src', '')

        if src:
            with open(src, 'rb') as src_file:
                files = {'src': (os.path.basename(src), src_file.read())}
        super().update(force_render, files, **kwargs)


class VideoWidget(Widget):
    extra_fields = [{'name': 'src'}]
    type = 'video'

    def update(self, force_render=False, files=None, **kwargs):
        src = kwargs.pop('src', '')

        if src:
            with open(src, 'rb') as src_file:
                files = {'src': (os.path.basename(src), src_file.read())}

        super().update(force_render, files, **kwargs)


class GroupWidget(Widget):
    type = 'group'
