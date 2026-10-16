from rest_framework.viewsets import ModelViewSet
from core.models import Compra
from core.serializers import CompraSerializer, CompraListRetrieveSerializer

class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.select_related("usuario").prefetch_related("itens__livro")
    serializer_class = CompraSerializer

    def get_serializer_class(self):
        if self.action in {"list", "retrieve"}:
            return CompraListRetrieveSerializer
        return CompraSerializer
