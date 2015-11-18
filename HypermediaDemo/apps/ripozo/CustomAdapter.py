import json
from ripozo.adapters import AdapterBase
from ripozo.resources.constants import input_categories
from ripozo.resources.resource_base import create_url
from ripozo.utilities import titlize_endpoint
import six

_CONTENT_TYPE = 'application/json'

class CustomAdapter(AdapterBase):

    formats = ['json', _CONTENT_TYPE]
    extra_headers = {'Content-Type': _CONTENT_TYPE}

    @property
    def formatted_body(self):
        if self.status_code == 204:
            return ''

        links = self.generate_links()
        entities = self.get_entities()
        response = dict(properties=self.resource.properties, actions=self._actions,
                        links=links, datas=entities)
        return json.dumps(response)

    @property
    def _actions(self):
        actions = []
        for endpoint, options in six.iteritems(self.resource.endpoint_dictionary()):
            options = options[0]
            all_methods = options.get('methods', ('GET',))
            meth = all_methods[0] if all_methods else 'GET'
            base_route = options.get('route', self.resource.base_url)
            route = create_url(base_route, **self.resource.properties)
            route = self.combine_base_url_with_resource_url(route)
            fields = self.generate_fields_for_endpoint_funct(options.get('endpoint_func'))
            actn = dict(name=endpoint, title=titlize_endpoint(endpoint),
                        method=meth, href=route, fields=fields)
            actions.append(actn)
        return actions

    def generate_fields_for_endpoint_funct(self, endpoint_func):
        return_fields = []
        fields_method = getattr(endpoint_func, 'fields', None)
        if not fields_method:
            return []
        fields = fields_method(self.resource.manager)

        for field in fields:
            if field.arg_type is input_categories.URL_PARAMS:
                continue
            field_dict = dict(name=field.name, type=field.field_type.__name__,
                              location=field.arg_type, required=field.required)
            return_fields.append(field_dict)
        return return_fields

    def generate_links(self):
        href = self.combine_base_url_with_resource_url(self.resource.url)
        links = [dict(rel=['self'], href=href)]
        for link, link_name, embedded in self.resource.linked_resources:
            links.append(dict(rel=[link_name],
                              href=self.combine_base_url_with_resource_url(link.url)))
        return links

    def get_entities(self):
        entities = []
        for resource, name, embedded in self.resource.related_resources:
            for ent in self.generate_entity(resource, name, embedded):
                entities.append(ent)
        return entities

    def generate_entity(self, resource, name, embedded):
        if isinstance(resource, list):
            for res in resource:
                for ent in self.generate_entity(res, name, embedded):
                    yield ent
        else:
            if not resource.has_all_pks:
                return
            ent = {}#{'class': [resource.resource_name], 'rel': [name]}
            resource_url = self.combine_base_url_with_resource_url(resource.url)
            if not embedded:
                ent['href'] = resource_url
                ent['data'] = resource.properties
            else:
                pass
                #ent['properties'] = resource.properties
                #ent['links'] = [dict(rel=['self'], href=resource_url)]
            yield ent

    @classmethod
    def format_exception(cls, exc):
        status_code = getattr(exc, 'status_code', 500)
        body = {'class': ['exception', exc.__class__.__name__],
                'actions': [], 'entities': [], 'links': [],
                'properties': dict(status=status_code, message=six.text_type(exc))}
        return json.dumps(body), cls.formats[0], status_code

    @classmethod
    def format_request(cls, request):
        return request