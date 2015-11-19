import json
from ripozo import ListRelationship, Relationship, apimethod
from apps.ripozo import CusRestmixins
from .managers import UserManager

class UserResource(CusRestmixins.CRUDL):
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
        #username = request.get('username')
        #return UserResource.query_string(username="root")
        #UserResource.get_entities()
        #return cls(properties=request.url_params, route_extension='extension/{0}'.format(1))
        return UserResource.get_entities()

#class TaskResource(restmixins.CRUD):
#    manager = TaskManager()
#    resource_name = 'task'
#    pks = ('id',)
#    _relationships = (
#        Relationship('task_board', property_map=dict(task_board_id='id'), relation='TaskBoardResource'),
#    )