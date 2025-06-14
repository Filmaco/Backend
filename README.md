#  Filmaço - Plataforma de Vídeos em FastAPI

Projeto desenvolvido em **Python 3.11** com **FastAPI**, oferecendo uma plataforma colaborativa de compartilhamento e visualização de vídeos nacionais.

---

##  Funcionalidades

- Cadastro e autenticação de usuários
- Upload e gerenciamento de vídeos (YouTube link)
- Criação e edição de playlists
- Sistema de comentários com notificações
- Reações a vídeos (Gostei, Não Gostei)
- Seguir e deixar de seguir usuários
- Busca avançada por filtros
- Sistema de denúncias com moderação
- Painel com estatísticas para usuários e admins

---

##  Tecnologias Utilizadas

- **Python 3.8.10**
- **FastAPI 0.110**
- **Uvicorn** (servidor ASGI)
- **SQLAlchemy** (ORM)
- **Pydantic**
- **SQLite / PostgreSQL**
- **JWT** para autenticação
- **Alembic** (migrações)
- **Email e Websockets** para notificações

---

##  Requisitos de Instalação

- Python 3.8.10 ou superior
- Git
- Gerenciador de pacotes `pip`

---

## Estrutura do Projeto
```bash
/app
 ├── main.py
 ├── controllers/
 ├── models/
 ├── routes/
 ├── uploads/
 └── services/
```
## Endpoints principais

##  Como Instalar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/filmaço.git
cd filmaço

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
 ```

## Como Executar

```bash
uvicorn main:app --reload
```


## Documentação automática

Swagger UI
```bash
http://localhost:8000/docs 
```
ReDoc
```bash
http://localhost:8000/redoc
```

## Desenvolvedores

Lara Victoria Souza Pereira – GitHub

