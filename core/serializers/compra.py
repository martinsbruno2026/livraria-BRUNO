from django.db import transaction
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    DecimalField,
    HiddenField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from core.models import Compra, ItensCompra

# ====================================================================
# Itens Compra
# ====================================================================


class ItensCompraCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')

    def validate_quantidade(self, quantidade):
        if quantidade <= 0:
            raise ValidationError('A quantidade deve ser maior do que zero.')
        return quantidade

    def validate(self, item):
        if item['quantidade'] > item['livro'].quantidade:
            raise ValidationError('Quantidade de itens maior do que a quantidade em estoque.')
        return item


class ItensCompraListSerializer(ModelSerializer):
    livro = CharField(source='livro.titulo', read_only=True)

    class Meta:
        model = ItensCompra
        fields = ('livro', 'quantidade', 'preco')


class ItensCompraSerializer(ModelSerializer):
    titulo = CharField(source='livro.titulo', read_only=True)
    editora = CharField(source='livro.editora.nome', read_only=True)

    capa = CharField(source='livro.capa.url', read_only=True)

    total = SerializerMethodField()

    def get_total(self, item):
        return item.preco * item.quantidade

    class Meta:
        model = ItensCompra
        fields = ('id', 'titulo', 'editora', 'quantidade', 'preco', 'total', 'capa')


# ====================================================================
# Compra
# ====================================================================

class CompraCreateUpdateSerializer(ModelSerializer):
    usuario = HiddenField(default=CurrentUserDefault())
    itens = ItensCompraCreateUpdateSerializer(many=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')

    @transaction.atomic
    def create(self, validated_data):
        itens = validated_data.pop('itens')
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            item['preco'] = item['livro'].preco
            ItensCompra.objects.create(compra=compra, **item)
        return compra

    @transaction.atomic
    def update(self, compra, validated_data):
        itens = validated_data.pop('itens', None)
        if itens is not None:
            compra.itens.all().delete()
            for item in itens:
                item['preco'] = item['livro'].preco
                ItensCompra.objects.create(compra=compra, **item)
        return super().update(compra, validated_data)


class CompraListSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    itens = ItensCompraListSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'itens')


class CompraSerializer(ModelSerializer):
    usuario = CharField(source='usuario.email', read_only=True)
    status = CharField(source='get_status_display', read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ('id', 'usuario', 'status', 'total', 'itens')

from rest_framework import serializers
from .models import Compra

class CompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compra
        fields = ['id', 'data_criacao', 'data_atualizacao', 'outros_campos...']
       
