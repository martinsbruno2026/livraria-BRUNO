from django.db import models

class Categoria(models.Model):
    descricao = models.CharField("descrição", max_length=100)

    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        ordering = ["descricao"]

    def __str__(self):
        return self.descricao
