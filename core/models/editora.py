from django.db import models

class Editora(models.Model):
    nome = models.CharField("nome", max_length=100)
    site = models.URLField("site", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "editora"
        verbose_name_plural = "editoras"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
