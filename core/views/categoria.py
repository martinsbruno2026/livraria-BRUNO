from rest_framework.viewsets import ModelViewSet
from core.models import Categoria
from core.serializers import CategoriaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    search_fields = ["descricao"]
    ordering_fields = ["id", "descricao"]
