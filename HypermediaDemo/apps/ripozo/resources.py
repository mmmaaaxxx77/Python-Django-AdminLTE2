import json
from ripozo import restmixins, ListRelationship, Relationship, apimethod
from .managers import UserManager

class UserResource(restmixins.CRUDL):
    manager = UserManager()
    resource_name = 'user'
    pks = ('username',)
    #_relationships = (
    #    ListRelationship('task_set', relation='TaskResource'),
    #)

    # We're going to add a simple way to add
    # tasks to a board by extending the
    @apimethod(route='/editUser', methods=['POST'])
    def edit_user(cls, request):
        body_args = json.loads(request.body)
        email = body_args.get('email')
        return UserResource.update({email:email})

    @apimethod(route='/getUser', methods=['GET'])
    def get_user(cls, request):
        username = '' if 'username' not in request.GET else request.GET['username']
        return UserResource.query_string(username=username)

#class TaskResource(restmixins.CRUD):
#    manager = TaskManager()
#    resource_name = 'task'
#    pks = ('id',)
#    _relationships = (
#        Relationship('task_board', property_map=dict(task_board_id='id'), relation='TaskBoardResource'),
#    )