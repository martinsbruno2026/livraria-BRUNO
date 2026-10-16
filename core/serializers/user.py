from rest_framework.serializers import CharField, ModelSerializer, SlugRelatedField

from core.models import User
from uploader.models import Image
from uploader.serializers import ImageSerializer


class UserSerializer(ModelSerializer):
    foto_attachment_key = SlugRelatedField(
        source='foto',
        queryset=Image.objects.all(),
        slug_field='attachment_key',
        required=False,
        write_only=True,
    )
    foto = ImageSerializer(
        required=False,
        read_only=True
    )
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'foto',
            'foto_attachment_key',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'groups')
        depth = 1


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
