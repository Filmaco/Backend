#  Filmaço - Plataforma de Vídeos em FastAPI

Projeto desenvolvido em **Python 3.8.10** com **FastAPI**, oferecendo uma plataforma colaborativa de compartilhamento e visualização de vídeos nacionais.

---

## Desenvolvedora

Lara Victoria Souza Pereira – GitHub

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
- **MySQL**
- **JWT** para autenticação
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

#  Manual da API - Projeto FastAPI

Este projeto é uma API desenvolvida com **FastAPI 0.1.0** (OpenAPI 3.1), focada na gestão de usuários, vídeos, playlists e interações sociais. Abaixo estão listados os principais endpoints organizados por funcionalidade.

## Autenticação & Usuários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/usuarios/add` | Criar novo usuário |
| PUT | `/usuarios/editar/{usuario_id}` | Atualizar dados do usuário |
| PUT | `/usuarios/status/{usuario_id}/{status}` | Alterar status (ativo/inativo) |
| PUT | `/usuarios/promover/{admin_id}/{usuario_id_promovido}/{tipo}` | Promover tipo de usuário |
| GET | `/usuarios` | Listar todos os usuários |
| POST | `/usuarios/login` | Login com JWT |
| GET | `/perfil` | Obter perfil do usuário autenticado |
| GET | `/usuarios/{usuario_id}` | Obter usuário por ID |
| GET | `/usuarios/nome/{nome_completo}` | Buscar usuário por nome |

## Vídeos

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/videos/add` | Adicionar vídeo |
| PUT | `/videos/editar/{video_id}` | Editar vídeo |
| PUT | `/videos/status/{video_id}/{status}` | Inativar vídeo |
| POST | `/videos/{video_id}/visualizacao` | Adicionar visualização |
| GET | `/videos/` | Listar todos os vídeos |
| GET | `/videos/usuario/{usuario_id}` | Listar vídeos de um usuário |
| GET | `/videos/usuario/ativos/{usuario_id}` | Listar vídeos ativos de um usuário |
| GET | `/videos/{video_id}` | Obter detalhes de um vídeo |
| GET | `/videos/tipo/{tipo}` | Filtrar por tipo |
| GET | `/videos/tag/{nome_tag}` | Buscar por nome da tag |
| GET | `/videos/tag/id/{id_tag}` | Buscar nome da tag por ID |
| GET | `/videos/genero/{genero}` | Filtrar por gênero |
| GET | `/videos/tags` | Listar todas as tags cadastradas |

## Playlists

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/playlists/add` | Criar nova playlist |
| PUT | `/playlists/editar/{playlist_id}` | Atualizar playlist |
| DELETE | `/playlists/excluir/{playlist_id}` | Excluir playlist |
| POST | `/playlists/video/add` | Adicionar vídeo à playlist |
| PUT | `/playlists/video/remover` | Remover vídeo da playlist |
| GET | `/playlists/usuario/{usuario_id}` | Listar playlists de um usuário |

## Comentários

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/comentarios/add` | Adicionar comentário |
| GET | `/comentarios/video/{video_id}` | Listar comentários de um vídeo |
| DELETE | `/comentarios/excluir/{comentario_id}/{usuario_id}` | Excluir comentário |

## Seguidores

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/seguidores/seguir/{seguidor_id}/{seguido_id}` | Seguir um usuário |
| POST | `/seguidores/deixar_de_seguir/{seguidor_id}/{seguido_id}` | Deixar de seguir |
| GET | `/seguidores/listar/{usuario_id}` | Listar seguidores |

## Avaliações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/avaliacoes/add` | Avaliar vídeo |
| PUT | `/avaliacoes/editar/{avaliacao_id}` | Editar avaliação |
| DELETE | `/avaliacoes/excluir/{avaliacao_id}` | Excluir avaliação |
| GET | `/avaliacoes/listar/{video_id}` | Listar avaliações de um vídeo |
| GET | `/avaliacoes/usuario/{usuario_id}/{video_id}` | Última avaliação do usuário |
| GET | `/avaliacoes/usuarios/video/{video_id}` | Últimas avaliações dos usuários |

## Estatísticas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/estatisticas/usuarios/{usuario_id}` | Estatísticas do usuário |
| GET | `/estatisticas/seguidores/{usuario_id}` | Estatísticas dos seguidores |
| GET | `/estatisticas/seguidos/{usuario_id}` | Estatísticas dos seguidos |

## Busca Avançada

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/busca/videos` | Buscar vídeos por filtros combinados |
| GET | `/busca/tipo/{tipo}` | Buscar vídeos por tipo |

## Denúncias

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/denuncias/` | Criar denúncia |
| GET | `/denuncias/lista` | Listar denúncias |
| GET | `/denuncias/{denuncia_id}` | Detalhes da denúncia |
| PUT | `/denuncias/{denuncia_id}/status` | Atualizar status da denúncia |
| DELETE | `/denuncias/{denuncia_id}/remover-conteudo` | Remover conteúdo denunciado |

---

 **Atualizado em:** 14 de junho de 2025  
 **Base da API:** `http://localhost:8000`  
 **Documentação Swagger:** [`/docs`](http://localhost:8000/docs)  
 **Documentação Redoc:** [`/redoc`](http://localhost:8000/redoc)

