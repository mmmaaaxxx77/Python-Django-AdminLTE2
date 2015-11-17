from django_ripozo import DjangoDispatcher
from ripozo.adapters import SirenAdapter, HalAdapter
from .resources import UserResource

dispatcher = DjangoDispatcher(base_url='/apii')
dispatcher.register_resources(UserResource)
dispatcher.register_adapters(SirenAdapter, HalAdapter)

urlpatterns = dispatcher.url_patterns