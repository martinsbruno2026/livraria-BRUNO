from django.db import models
from .categoria import Categoria
from .editora import Editora
from .autor import Autor

class Livro(models.Model):
    titulo = models.CharField("título", max_length=255)
    isbn = models.CharField("ISBN", max_length=32, null=True, blank=True)
    quantidade = models.IntegerField("quantidade em estoque", default=0, null=True, blank=True)
    preco = models.DecimalField("preço", max_digits=7, decimal_places=2, default=0)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="livros",
        null=True, blank=True
    )
    editora = models.ForeignKey(
        Editora, on_delete=models.PROTECT, related_name="livros",
        null=True, blank=True
    )
    autores = models.ManyToManyField(Autor, related_name="livros", blank=True)

    class Meta:
        verbose_name = "livro"
        verbose_name_plural = "livros"
        ordering = ["titulo"]

    def __str__(self):
        return f"({self.id}) {self.titulo} ({self.quantidade})"
