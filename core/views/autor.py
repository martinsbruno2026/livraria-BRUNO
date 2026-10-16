from rest_framework.viewsets import ModelViewSet
from core.models import Autor
from core.serializers import AutorSerializer

class AutorViewSet(ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    search_fields = ["nome", "email"]
    ordering_fields = ["id", "nome"]
