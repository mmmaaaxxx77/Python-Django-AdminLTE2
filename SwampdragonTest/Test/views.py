import json
from django.http import HttpResponse
from swampdragon.pubsub_providers.data_publisher import publish_data


def index(request):
    data = {'name': 'name', 'message': 'message'}
    publish_data(channel='chatroom', data=data)
    return HttpResponse(json.dumps({}), content_type="application/javascript")
