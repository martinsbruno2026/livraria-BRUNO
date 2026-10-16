from django.db import models

class Autor(models.Model):
    nome = models.CharField("nome", max_length=100)
    email = models.EmailField("e-mail", max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "autor"
        verbose_name_plural = "autores"
        ordering = ["nome"]

    def __str__(self):
        return self.nome
