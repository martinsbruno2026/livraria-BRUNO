from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Categoria, Editora, Autor, Livro, Compra, ItemCompra

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    fieldsets = DjangoUserAdmin.fieldsets + (("Informações adicionais", {"fields": ()}),)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "descricao")
    search_fields = ("descricao",)

@admin.register(Editora)
class EditoraAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "site")
    search_fields = ("nome",)

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email")
    search_fields = ("nome", "email")

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "categoria", "editora", "preco", "quantidade")
    list_filter = ("categoria", "editora")
    search_fields = ("titulo", "isbn", "autores__nome")
    filter_horizontal = ("autores",)

class ItemCompraInline(admin.TabularInline):
    model = ItemCompra
    extra = 1

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "data")
    list_filter = ("data",)
    inlines = (ItemCompraInline,)

@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ("id", "compra", "livro", "quantidade", "preco_unitario")
