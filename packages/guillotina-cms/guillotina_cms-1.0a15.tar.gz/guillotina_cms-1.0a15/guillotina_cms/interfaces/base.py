import json

from guillotina import schema
from guillotina.directives import index_field
from guillotina_cms.directives import fieldset
from zope.interface import Interface


HISTORY_SCHEMA = json.dumps({
    'type': 'object',
    'properties': {
        'actor': {'type': 'string'},
        'comments': {'type': 'string'},
        'time': {'type': 'date'},
        'type': {'type': 'string'},
        'title': {'type': 'string'},
        'data': {'type': 'object'}
    }
})

# If its a workflow:
#     type: workflow
#     data:
#         action: string (action)
#         review_state: string (review state moved to)

# If its a versioning:
#     type: versioning
#         version: int (action)


class ICMSLayer(Interface):
    """Marker interface layer Plone.CMS."""


class ICMSBehavior(Interface):

    index_field('hidden_navigation', type='boolean')
    fieldset('hidden_navigation', 'settings')
    hidden_navigation = schema.Bool(
        title='Should be hidden on navigation',
        required=False,
        default=False)

    index_field('language', type='keyword')
    fieldset('language', 'categorization')
    language = schema.Choice(
        title='Language',
        required=False,
        source='languages')

    index_field('content_layout', type='keyword')
    fieldset('content_layout', 'settings')
    content_layout = schema.Choice(
        title='Content Layout',
        required=False,
        source='content_layouts',
        default='default')

    index_field('position_in_parent', type='int')
    position = schema.Int(
        title='Position in parent',
        required=False)

    index_field('review_state', type='keyword')
    review_state = schema.Choice(
        readonly=True,
        title='Workflow review state',
        required=False,
        source='worklow_states')

    history = schema.List(
        title='History list',
        readonly=True,
        required=False,
        value_type=schema.JSONField(
            title='History element',
            schema=HISTORY_SCHEMA))
