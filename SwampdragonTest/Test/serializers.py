from swampdragon.serializers.model_serializer import ModelSerializer


class FooSerializer(ModelSerializer):
    class Meta:
        model = 'myapp.Foo'
        publish_fields = ('text', )
        update_fields = ('text', )