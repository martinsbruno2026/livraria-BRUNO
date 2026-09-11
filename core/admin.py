"""
Django admin customization.
"""

from django.contrib.admin import ModelAdmin, StackedInline, display, register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import (
    Autor,
    Categoria,
    Compra,
    Editora,
    ItensCompra,
    Livro,
    User,
)


@register(Autor)
class AutorAdmin(ModelAdmin):
    list_display = ('nome', 'email')
    search_fields = ('nome', 'email')
    list_filter = ('nome',)
    ordering = ('nome', 'email')
    list_per_page = 10


@register(Categoria)
class CategoriaAdmin(ModelAdmin):
    list_display = ('descricao',)
    search_fields = ('descricao',)
    list_filter = ('descricao',)
    ordering = ('descricao',)
    list_per_page = 10


class ItensCompraInline(StackedInline):
    model = ItensCompra
    extra = 1  # Quantidade de itens adicionais


@register(Compra)
class CompraAdmin(ModelAdmin):
    list_display = ('usuario', 'status', 'total_formatado')
    search_fields = ('usuario', 'status')
    list_filter = ('usuario', 'status')
    ordering = ('usuario', 'status')
    list_per_page = 10
    inlines = [ItensCompraInline]
    readonly_fields = ('total_formatado',)

    @display(description="Total")
    def total_formatado(self, obj):
        """Exibe R$ 123,45 em vez de 123.45."""
        return f"R$ {obj.total:.2f}"

@register(Editora)
class EditoraAdmin(ModelAdmin):
    list_display = ('nome', 'email', 'cidade')
    search_fields = ('nome', 'email', 'cidade')
    list_filter = ('nome', 'email', 'cidade')
    ordering = ('nome', 'email', 'cidade')
    list_per_page = 10


@register(Livro)
class LivroAdmin(ModelAdmin):
    list_display = ('titulo', 'editora', 'categoria', 'preco', 'quantidade')
    search_fields = ('titulo', 'editora__nome', 'categoria__descricao')
    list_filter = ('editora', 'categoria')
    ordering = ('titulo', 'editora', 'categoria')
    list_per_page = 25


@register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ('id',)
    list_display = ('email', 'name')
    search_fields = ('email', 'name', 'groups__name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'foto',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('Groups'), {'fields': ('groups',)}),
        (_('User Permissions'), {'fields': ('user_permissions',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'password1',
                    'password2',
                    'name',
                    'foto',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )
