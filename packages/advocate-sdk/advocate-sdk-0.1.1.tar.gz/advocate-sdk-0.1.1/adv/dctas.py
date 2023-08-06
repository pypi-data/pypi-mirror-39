import os

from . import widgets
from .events import Event, EVENT_TYPES
from .exceptions import UpdateError, APIException, RenderError


def class_from_type(type_string):
    """
    Converts a widget type to it's respective class. For example, 'text'
    would become 'TextWidget'
    """
    class_name = '{}{}Widget'.format(type_string[0].upper(), type_string[1:])
    return getattr(widgets, class_name)


class DCTA:
    def __init__(
        self, client, id=None, name='', widgets=None, global_styles=None,
        component=None, events=None
    ):
        self.client = client

        self.id = id
        self.global_styles = {} if global_styles is None else global_styles
        self.name = name
        self.component = component

        self.widgets = [] if widgets is None else widgets
        self.events = [] if events is None else events

    def __repr__(self):
        return '<DCTA: {}>'.format(self)

    def __str__(self):
        return self.name

    @classmethod
    def deserialize(cls, client, dcta_data):
        """
        Deserializes DCTA from dictionary
        """
        widgets_data = dcta_data.pop('widgets', [])
        events_data = dcta_data.pop('events', [])

        dcta = cls(client, **dcta_data)
        client.dctas[dcta.id] = dcta

        for widget in widgets_data:
            widget_class = class_from_type(widget['type'])
            widget['dcta'] = dcta.id
            dcta.widgets.append(widget_class.deserialize(client, widget))

        for event in events_data:
            event['dcta'] = dcta.id
            dcta.events.append(Event.deserialize(client, event))

        return dcta

    def serialize(self):
        """
        Converts DCTA data and contained widgets to dicts, for easy serialization
        """
        data = {
            'global_styles': self.global_styles,
            'name': self.name,
            'widgets': [],
            'events': [],
            'id': self.id,
            'component': self.component,
        }

        for widget in self.widgets:
            data['widgets'].append(widget.serialize())

        for event in self.events:
            data['events'].append(event.serialize())

        return data

    def add_text_widget(self, text='', **kwargs):
        """
        Creates a new TextWidget on this DCTA
        """
        if not text:
            raise UpdateError('`text` is a required kwarg for `add_text_widget`')

        self._add_widget('text', text=text, **kwargs)

    def add_image_widget(self, src='', **kwargs):
        """
        Creates a new ImageWidget on this DCTA
        """
        if not src:
            raise UpdateError('`src` is a required kwarg for `add_image_widget`')

        with open(src, 'rb') as src_file:
            self._add_widget('image', files={'src': (os.path.basename(src), src_file)}, **kwargs)

    def add_video_widget(self, src='', **kwargs):
        """
        Creates a new ImageWidget on this DCTA
        """
        if not src:
            raise UpdateError('`src` is a required kwarg for `add_video_widget`')

        with open(src, 'rb') as src_file:
            self._add_widget('video', files={'src': (os.path.basename(src), src_file)}, **kwargs)

    def add_group_widget(self, **kwargs):
        """
        Creates a new GroupWidget on this DCTA
        """
        self._add_widget('group', **kwargs)

    def _add_widget(self, type, force_render=False, broadcasters=[], files=None, **kwargs):
        """
        Creates a widget of a given type on a DCTA
        """
        force_render = kwargs.pop('force_render', False)

        new_widget_data = {
            'broadcasters': broadcasters,
            'dcta': self.id,
            **kwargs,
        }

        try:
            widget_data = self.client.post('widgets/{}/'.format(type), data=new_widget_data, files=files)
        except APIException as error:
            raise UpdateError(
                'Could not create new {} widget: {}'.format(type, error.message)
            )

        widget_class = class_from_type(type)
        widget = widget_class.deserialize(self.client, widget_data)

        self.widgets.append(widget)

        if force_render:
            self.render()

        return widget

    def add_command_event(self, command=None, response_url=None):
        """
        Adds an Event with type `CC` (aka Chatbot Command)
        """
        for kwarg in [command, response_url]:
            assert kwarg is not None, (
                '"{}" is a required argument for `add_command_event`'
            )
        return self._add_event(
            'CC', event_data=command, response_url=response_url
        )

    def _add_event(self, event_type, **kwargs):
        """
        Creates an Event of a given type
        """
        new_event_data = {
            'event_type': event_type,
            'dcta': self.id,
            **kwargs,
        }

        try:
            event_data = self.client.post(
                'dcta-events/', data=new_event_data,
            )
        except APIException as error:
            raise UpdateError(
                'Could not create new {} event_type: {}'.format(
                    EVENT_TYPES[event_type], error.message
                )
            )

        event = Event.deserialize(self.client, event_data)
        self.events.append(event)

        return event

    def render(self):
        """
        Triggers a (re)-render of the DCTA for all live browsersources
        """
        try:
            self.client.post('dctas/{}/render/'.format(self.id), {})
        except APIException as error:
            raise RenderError(
                'Unable to render DCTA: {}'.format(error.message)
            )

    def update(self, force_render=False, **kwargs):
        """
        Updates a DCTA's data on the server (and locally). User `force_render` to
        render the DCTA to all active browsersources when the update is done
        """
        new_data = {}

        for key, value in kwargs.items():
            new_data[key] = value

        try:
            updated_data = self.client.patch('dctas/{}/'.format(self.id), new_data)
        except APIException as error:
            raise UpdateError(
                'Could not update widget: {}'.format(error.message)
            )

        # Widgets can't be updated via the DCTA `update`, so we can safely remove
        # redundant widget data
        updated_data.pop('widgets', '')

        for key, value in updated_data.items():
            setattr(self, key, value)

        if force_render:
            self.render()

        return self
