from rest_framework import serializers
from core.models import Compra, ItemCompra

class ItemCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCompra
        fields = ["id", "livro", "quantidade", "preco_unitario"]
        read_only_fields = ["id"]

class CompraSerializer(serializers.ModelSerializer):
    itens = ItemCompraSerializer(many=True)

    class Meta:
        model = Compra
        fields = ["id", "usuario", "data", "observacao", "itens"]
        read_only_fields = ["id", "data"]

    def create(self, validated_data):
        itens_data = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item in itens_data:
            if "preco_unitario" not in item:
                item["preco_unitario"] = item["livro"].preco
            ItemCompra.objects.create(compra=compra, **item)
        return compra

    def update(self, instance, validated_data):
        itens_data = validated_data.pop("itens", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if itens_data is not None:
            instance.itens.all().delete()
            for item in itens_data:
                if "preco_unitario" not in item:
                    item["preco_unitario"] = item["livro"].preco
                ItemCompra.objects.create(compra=instance, **item)
        return instance

class CompraListRetrieveSerializer(serializers.ModelSerializer):
    itens = ItemCompraSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "usuario", "data", "observacao", "itens", "total"]
        depth = 1
