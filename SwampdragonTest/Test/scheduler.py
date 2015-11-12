from swampdragon.pubsub_providers.data_publisher import publish_data

print("123")
def my_task():
    print("123")
    data = {'name': 'name', 'message': 'message'}
    publish_data(channel='chatroom', data=data)

