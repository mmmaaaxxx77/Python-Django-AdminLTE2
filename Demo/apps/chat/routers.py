from swampdragon import route_handler
from swampdragon.permissions import login_required, LoginRequired
from swampdragon.route_handler import BaseRouter

class Chat(BaseRouter):
    route_name = 'chat'
    valid_verbs = BaseRouter.valid_verbs + ['say_hello', 'chat']
    #permission_classes = [LoginRequired()]

    def get_subscription_channels(self, **kwargs):
        return ['chatroom']

    @login_required
    def say_hello(self, **kwargs):
        data = {'name': kwargs['name'], 'message': 'hello'}
        self.publish(self.get_subscription_channels(), {'data': data})

    @login_required
    def chat(self, **kwargs):
        print(self.connection.get_user().is_authenticated())
        self.publish(self.get_subscription_channels(), {'data': kwargs})

route_handler.register(Chat)
