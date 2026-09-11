from rest_framework.viewsets import ModelViewSet

from core.models import Livro
from core.serializers import LivroListSerializer, LivroRetrieveSerializer, LivroSerializer


class LivroViewSet(ModelViewSet):
    queryset = Livro.objects.order_by('-id')
    serializer_class = LivroSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return LivroListSerializer
        elif self.action == 'retrieve':
            return LivroRetrieveSerializer
        return LivroSerializer
