from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter


class FooRouter(BaseRouter):
    route_name = 'foo'
    valid_verbs = BaseRouter.valid_verbs + ['say_hello']

    def get_subscription_channels(self, **kwargs):
        return ['chatroom']

    def say_hello(self, **kwargs):
        self.send({'message': 'hello'})
        self.publish(self.get_subscription_channels(), kwargs)


route_handler.register(FooRouter)
