from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Compra
from core.serializers import (
    CompraCreateUpdateSerializer,
    CompraListSerializer,
    CompraSerializer,
)


class CompraViewSet(ModelViewSet):
    queryset = Compra.objects.order_by("-id")
    serializer_class = CompraSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompraListSerializer
        if self.action in {'create', 'update'}:
            return CompraCreateUpdateSerializer
        return CompraSerializer

    def get_queryset(self):
        usuario = self.request.user
        if usuario.is_superuser:
            return Compra.objects.order_by('-id')
        if usuario.groups.filter(name='administradores'):
            return Compra.objects.order_by('-id')
        return Compra.objects.filter(usuario=usuario).order_by('id')

    @extend_schema(
        request=None,
        responses={200: None},
        description="Gera um relatório de vendas do mês atual.",
        summary="Relatório de vendas do mês",
    )
    @action(detail=False, methods=['get'])
    def relatorio_vendas_mes(self, request):
        agora = timezone.now()
        inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        compras = Compra.objects.filter(
                status=Compra.StatusCompra.FINALIZADO,
                data__gte=inicio_mes
        )

        total_vendas = sum(compra.total for compra in compras)
        quantidade_vendas = compras.count()

        return Response(
            {
                'status': 'Relatório de vendas deste mês',
                'total_vendas': total_vendas,
                'quantidade_vendas': quantidade_vendas,
            },
            status=status.HTTP_200_OK,
        )
