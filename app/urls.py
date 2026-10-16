from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.views import (
    CategoriaViewSet, EditoraViewSet, AutorViewSet, LivroViewSet,
    UserViewSet, CompraViewSet,
)

router = DefaultRouter()
router.register("categorias", CategoriaViewSet, basename="categoria")
router.register("editoras", EditoraViewSet, basename="editora")
router.register("autores", AutorViewSet, basename="autor")
router.register("livros", LivroViewSet, basename="livro")
router.register("users", UserViewSet, basename="user")
router.register("compras", CompraViewSet, basename="compra")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
