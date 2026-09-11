from .autor import AutorSerializer
from .categoria import CategoriaSerializer
from .compra import (
    ItensCompraCreateUpdateSerializer,
    ItensCompraListSerializer,
    ItensCompraSerializer,
    CompraCreateUpdateSerializer,
    CompraListSerializer,
    CompraSerializer,
)
from .editora import EditoraSerializer
from .livro import LivroListSerializer, LivroRetrieveSerializer, LivroSerializer
from .user import UserRegistrationSerializer, UserSerializer
