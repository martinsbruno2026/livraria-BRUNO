from rest_framework.viewsets import ModelViewSet
from core.models import Livro
from core.serializers import LivroSerializer, LivroListRetrieveSerializer

class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.select_related("categoria", "editora").prefetch_related("autores")
    serializer_class = LivroSerializer
    search_fields = ["titulo", "isbn", "autores__nome", "categoria__descricao", "editora__nome"]
    ordering_fields = ["id", "titulo", "preco", "quantidade"]

    def get_serializer_class(self):
        if self.action in {"list", "retrieve"}:
            return LivroListRetrieveSerializer
        return LivroSerializer
