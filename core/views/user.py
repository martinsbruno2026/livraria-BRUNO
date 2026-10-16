from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from core.models import User
from core.serializers import UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    search_fields = ["username", "email", "first_name", "last_name"]
