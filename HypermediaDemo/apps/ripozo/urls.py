#from django_ripozo import DjangoDispatcher
from ripozo.adapters import SirenAdapter, HalAdapter, BasicJSONAdapter
from .resources import UserResource
from .CustomAdapter import CustomAdapter
from .CustomDispatcher import DjangoDispatcher

dispatcher = DjangoDispatcher(base_url='/apii')
dispatcher.register_resources(UserResource)
dispatcher.register_adapters(CustomAdapter)

urlpatterns = dispatcher.url_patterns