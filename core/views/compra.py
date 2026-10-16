
from django.db import transaction
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
        responses={200: None, 400: None},
        description="Finaliza a compra, atualizando o estoque dos livros.",
        summary="Finalizar compra",
    )
    @action(detail=True, methods=["post"])
    @transaction.atomic
    def finalizar(self, request, pk=None):
        compra = self.get_object()

        # Verifica se a compra já foi finalizada
        if compra.status == Compra.StatusCompra.FINALIZADO:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={'status': 'Compra já finalizada'}
            )

        for item in compra.itens.all():

            # Valida se o estoque é suficiente para cada livro
            if item.quantidade > item.livro.quantidade:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={
                        'status': 'Quantidade insuficiente',
                        'livro': item.livro.titulo,
                        'quantidade_disponivel': item.livro.quantidade,
                    }
                )

            # Atualiza o estoque dos livros
            item.livro.quantidade -= item.quantidade
            item.livro.save()

        # Finaliza a compra: atualiza status
        compra.status = Compra.StatusCompra.FINALIZADO
        compra.save()

        return Response(status=status.HTTP_200_OK, data={'status': 'Compra finalizada'})

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
