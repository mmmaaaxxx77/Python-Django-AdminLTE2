from swampdragon.pubsub_providers.data_publisher import publish_data
import kronos


#@kronos.register('*:5 * * * *')
def mytask():
    print("123")
    f = open('/Users/johnnytsai/PythonProjects/Python-Django-AdminLTE2/SwampdragonTest/console.txt', 'a')
    f.write("123")
    data = {'name': 'name', 'message': 'message'}
    publish_data(channel='chatroom', data=data)
