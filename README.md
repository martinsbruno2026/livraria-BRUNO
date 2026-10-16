# Livraria — Django Admin + API REST

Projeto didático com Django, Django REST Framework, SQLite, painel Admin, JWT e documentação Swagger.

## Requisitos

- Python 3.11 ou superior
- Git (opcional)
- PDM

## Instalação

```bash
# Entre na pasta do projeto
cp .env.example .env
pdm install
pdm run migrate
pdm run seed-admin
pdm run dev
```

Se o comando `pdm` não existir, instale-o seguindo a documentação oficial do PDM e reinicie o terminal.

## Endereços

- Admin: http://127.0.0.1:8000/admin/
- API raiz: http://127.0.0.1:8000/api/
- Categorias: http://127.0.0.1:8000/api/categorias/
- Editoras: http://127.0.0.1:8000/api/editoras/
- Autores: http://127.0.0.1:8000/api/autores/
- Livros: http://127.0.0.1:8000/api/livros/
- Compras: http://127.0.0.1:8000/api/compras/
- Swagger: http://127.0.0.1:8000/api/swagger/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- Schema OpenAPI: http://127.0.0.1:8000/api/schema/

## Acesso de demonstração ao Admin

Depois de executar `pdm run seed-admin`:

- E-mail: `a@a.com`
- Senha: `teste.123`

Essas credenciais são apenas para desenvolvimento local. Troque a senha e não publique este usuário em um servidor real.

## Entidades

- `Categoria`: descrição.
- `Editora`: nome e site opcional.
- `Autor`: nome e e-mail opcional.
- `Livro`: título, ISBN, quantidade, preço, categoria, editora e vários autores.
- `User`: usuário customizado com e-mail único.
- `Compra`: usuário, data e observação.
- `ItemCompra`: livro, quantidade e preço unitário.

## API REST

Os endpoints de recursos usam `ModelViewSet`, então disponibilizam GET, POST, PUT, PATCH e DELETE. O endpoint `users` exige autenticação de administrador.

### Exemplo: criar uma categoria

```http
POST /api/categorias/
Content-Type: application/json

{
  "descricao": "Ficção"
}
```

### Exemplo: criar uma editora

```json
{
  "nome": "Editora Exemplo",
  "site": "https://example.com"
}
```

### Exemplo: criar um livro

Os campos `categoria`, `editora` e `autores` recebem IDs. Exemplo:

```json
{
  "titulo": "Diário de um Banana",
  "isbn": "9788576831300",
  "quantidade": 12,
  "preco": "39.90",
  "categoria": 1,
  "editora": 1,
  "autores": [1]
}
```

### Autenticação JWT

Solicite tokens em `POST /api/token/` com JSON contendo `username` e `password`. Use o `access` recebido como `Authorization: Bearer <token>`. Para renovar, envie `refresh` para `POST /api/token/refresh/`.

## Observações

- Banco SQLite criado localmente após as migrações.
- `on_delete=PROTECT` impede apagar categorias/editoras/autores/livros que ainda tenham relacionamentos protegidos.
- A API permite CORS para `localhost:3000` e `127.0.0.1:3000`; altere `.env` se necessário.
- Não use as credenciais de demonstração em produção.
