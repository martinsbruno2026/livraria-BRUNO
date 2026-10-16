from django.conf import settings
from django.db import models
from .livro import Livro

class Compra(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="compras"
    )
    data = models.DateTimeField("data da compra", auto_now_add=True)
    observacao = models.TextField("observação", blank=True)

    class Meta:
        verbose_name = "compra"
        verbose_name_plural = "compras"
        ordering = ["-data"]

    def __str__(self):
        return f"Compra #{self.pk} - {self.usuario}"

    @property
    def total(self):
        return sum((item.subtotal for item in self.itens.all()), start=0)

class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(Livro, on_delete=models.PROTECT, related_name="itens_compra")
    quantidade = models.PositiveIntegerField("quantidade", default=1)
    preco_unitario = models.DecimalField("preço unitário", max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = "item da compra"
        verbose_name_plural = "itens da compra"

    def save(self, *args, **kwargs):
        if self.preco_unitario is None:
            self.preco_unitario = self.livro.preco
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade} x {self.livro.titulo}"
