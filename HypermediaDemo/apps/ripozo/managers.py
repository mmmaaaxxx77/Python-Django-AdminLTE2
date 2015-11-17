from django_ripozo import DjangoManager
from django.contrib.auth.models import User


class UserManager(DjangoManager):
    # These are the default fields to use when performing any action
    fields = ('username', 'email',)
    update_fields = ('email',) # These are the only fields allowed when updating.
    model = User
    paginate_by = 2

#class TaskManager(DjangoManager):
#    fields = ('id', 'title', 'description', 'completed', 'task_board_id',)
#    model = Task
#    paginate_by = 20