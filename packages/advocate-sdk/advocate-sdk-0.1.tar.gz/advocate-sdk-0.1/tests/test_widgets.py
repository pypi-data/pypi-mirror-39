from unittest import TestCase
from unittest.mock import patch

from adv.widgets import Widget, TextWidget, ImageWidget, GroupWidget
from adv.client import AdvClient
from adv.dctas import DCTA


class WidgetTests(TestCase):
    def setUp(self):
        self.client = AdvClient('test-api-key')
        self.dcta = DCTA(self.client, id=15, name='Test DCTA', widgets=[])
        self.client.dctas[15] = self.dcta

    def test_simple_deserialization(self):
        """
        passing `deserialize` an advocate client and valid widget data
        should create a Widget object with the appropriate values set
        """
        widget_data = {
            'parent': 2,
            'attributes': {
                'class': 'my-widget',
            },
            'styles': {
                'position': 'absolute',
                'top': '50%',
            },
            'dcta': self.dcta.id,
        }

        widget = Widget.deserialize(self.client, widget_data)

        self.assertEqual(widget.parent, 2)
        self.assertEqual(widget.attributes, {'class': 'my-widget'})
        self.assertEqual(widget.styles, {'position': 'absolute', 'top': '50%'})
        self.assertEqual(widget.broadcasters, [])
        self.assertEqual(widget.dcta, self.dcta)

    def test_deserialization_with_extra_fields(self):
        """
        subclassing Widget and adding `extra_fields` should allow deserialization
        for the extra fields in addition to the standard widget
        fields
        """
        class ExtraFieldWidget(Widget):
            extra_fields = [
                {'name': 'test_field', 'default': 'some value'},
                {'name': 'another_field'}
            ]

        widget_data = {
            'parent': 1,
            'dcta': self.dcta.id,
        }

        widget = ExtraFieldWidget.deserialize(self.client, widget_data)

        self.assertEqual(widget.parent, 1)
        self.assertEqual(widget.attributes, {})
        self.assertEqual(widget.styles, {})
        self.assertEqual(widget.test_field, 'some value')
        self.assertIsNone(widget.another_field)

    def test_TextWidget_creates_text_field(self):
        """
        TextWidget should create a text attribute, even if nothing is passed in
        """
        widget = TextWidget.deserialize(self.client, {'dcta': self.dcta.id})
        self.assertEqual(widget.text, '')

    def test_ImageWidget_creates_src_field(self):
        """
        ImageWidget should create a src attribute, even if nothing is passed in
        """
        widget = ImageWidget.deserialize(self.client, {'dcta': self.dcta.id})
        self.assertIsNone(widget.src)

    def test_basic_serialize(self):
        """
        A Widget's `serialize` function should transform all relevant data, including the widget
        "type", into a dictionary
        """
        widget = Widget(
            self.client,
            parent=1,
            styles={'top': '50%', 'left': '10px'},
            dcta=self.dcta.id,
            id=10,
            name='Test Widget',
        )

        expected_data = {
            'name': 'Test Widget',
            'parent': 1,
            'styles': {'top': '50%', 'left': '10px'},
            'attributes': {},
            'type': '',
            'broadcasters': [],
            'dcta': self.dcta.id,
            'id': 10,
        }

        self.assertEqual(widget.serialize(), expected_data)

    @patch('adv.client.AdvClient.patch')
    def test_update_fills_in_missing_data_for_put(self, mock_put):
        """
        Calling the `update` function on a widget should fill in the rest of the data
        from the widget, so that only the specific kwargs that need updating need to be passed
        into the function
        """
        base_widget_data = {
            'parent': 1,
            'styles': {'top': '50%', 'left': '10px'},
            'dcta': self.dcta.id,
            'id': 10,
            'name': 'Test Widget',
            'attributes': {'class': 'my-widget'},
            'broadcasters': [],
            'text': 'Hello World',
        }

        widget = TextWidget(
            self.client,
            **base_widget_data,
        )

        widget.update(text='Jello Unfurled')

        mock_put.assert_called_with('widgets/text/10/', {'text': 'Jello Unfurled'}, files=None)

    def test_type_generation(self):
        """
        The `type` property should generate the proper type text
        """
        widget = TextWidget(self.client, text='dummy text', dcta=self.dcta.id)
        self.assertEqual(widget.type, 'text')

        widget = ImageWidget(self.client, src='https://my/image.jpg', dcta=self.dcta.id)
        self.assertEqual(widget.type, 'image')

        widget = GroupWidget(self.client, dcta=self.dcta.id)
        self.assertEqual(widget.type, 'group')

    @patch('adv.client.AdvClient.patch')
    def test_update_single_style(self, mock_patch):
        """
        calling `update_style` should keep all styles the same except the
        single style to be updated
        """
        base_widget_data = {
            'parent': 1,
            'styles': {
                'position': 'absolute',
                'top': '50%',
                'left': '10px',
            },
            'dcta': self.dcta.id,
            'id': 10,
            'name': 'Test Widget',
            'attributes': {'class': 'my-widget'},
            'broadcasters': [],
            'text': 'Hello World',
        }

        widget = TextWidget(
            self.client,
            **base_widget_data,
        )

        widget.update_style('left', '25px')

        mock_patch.assert_called_with(
            'widgets/text/10/',
            {'styles': {
                'position': 'absolute',
                'top': '50%',
                'left': '25px',
            }},
            files=None,
        )
