from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter


class Chat(BaseRouter):
    route_name = 'chat'
    valid_verbs = BaseRouter.valid_verbs + ['say_hello', 'chat']

    def get_subscription_channels(self, **kwargs):
        return ['chatroom']

    def say_hello(self, **kwargs):
        data = {'name': kwargs['name'], 'message': 'hello'}
        self.publish(self.get_subscription_channels(), {'data': data})

    def chat(self, **kwargs):
        self.publish(self.get_subscription_channels(), {'data': kwargs})


route_handler.register(Chat)
