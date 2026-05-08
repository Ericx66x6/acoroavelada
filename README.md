# A Coroa Velada

Descrição curta para GitHub:

> Plataforma web de fichas para Vampiro: A Máscara com backend próprio, gerenciamento de personagens, XP, rituais, disciplinas e sistema persistente em JSON.

---

# A Coroa Velada

Sistema web completo feito para campanhas de Vampiro: A Máscara.

O projeto inclui frontend, backend e ferramentas administrativas para gerenciamento de fichas online, personagens, disciplinas, rituais, XP e dados globais da campanha.

O sistema foi criado para permitir que jogadores acessem fichas diretamente pelo navegador enquanto o mestre controla os dados através de um backend simples e flexível.

Funcionalidades principais:

* fichas online
* persistência em JSON
* gerenciamento de XP
* disciplinas
* rituais
* sistema de status
* dados globais da campanha
* upload/download de personagens
* painel administrativo via terminal
* API própria para integração frontend/backend

---

# Tecnologias

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* Python
* Flask
* Flask-CORS
* JSON
* Requests
* Gunicorn

---

# Estrutura do Projeto

````txt
A-Coroa-Velada/
│
├── frontend/
│   ├── sheet.html
│   ├── js/
│   ├── css/
│   └── assets/
│
├── backend/
│   ├── app.py
│   ├── admin.py
│   ├── requirements.txt
│   │
│   └── json/
│       ├── game_data.json
│       │
│       └── characters/
│           ├── bella.json
│           ├── lucien.json
│           └── ...
```txt
A-Coroa-Velada/
│
├── app.py
├── admin.py
├── requirements.txt
│
├── json/
│   ├── game_data.json
│   │
│   └── characters/
│       ├── bella.json
│       ├── lucien.json
│       └── ...
````

---

# Funcionalidades

## Sistema de Fichas

* atributos
* disciplinas
* rituais
* humanidade
* geração
* XP
* status personalizados
* atualização em tempo real via API

---

## Frontend

* carregamento automático via URL
* integração com fetch
* leitura de JSON remoto
* renderização dinâmica de fichas

Exemplo:

```txt
sheet.html?char=bella&token=TOKEN
```

---

## Backend

## API

### GET `/game`

Retorna os dados globais do jogo.

---

### GET `/get`

Retorna os dados de um personagem.

Parâmetros:

```txt
char
 token
```

---

### POST `/save`

Salva completamente a ficha de um personagem.

---

### POST `/addxp`

Adiciona XP ao personagem.

---

### POST `/changegeneration`

Altera a geração do personagem.

---

### GET `/listchars`

Lista todos os personagens.

---

### POST `/upload/<name>`

Faz upload de um JSON de personagem.

---

### GET `/download/<name>`

Baixa o JSON de um personagem.

---

### DELETE `/delete/<name>`

Deleta um personagem.

---

# Instalação

## 1. Clone o projeto

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPO.git
```

---

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 3. Rode o servidor

```bash
python app.py
```

Servidor:

```txt
http://127.0.0.1:5000
```

---

# Deploy no Render

## Build Command

```txt
pip install -r requirements.txt
```

## Start Command

```txt
gunicorn app:app
```

---

# Console Administrativo

O projeto inclui um console administrativo em terminal (`admin.py`) para:

* dar XP
* dar XP da sessão
* mudar geração
* listar personagens
* upload/download de JSON
* deletar personagens
* backup do game_data
* upload do game_data

---

# Segurança

O sistema utiliza autenticação simples por token.

Exemplo:

```python
TOKEN = "seu_token"
```

---

# Objetivo do Projeto

O foco do projeto é ser um sistema simples, rápido e extremamente fácil de modificar.

Ao invés de banco de dados complexo, o sistema utiliza arquivos JSON diretamente, facilitando:

* edição manual
* backup
* balanceamento rápido
* criação de conteúdo
* prototipagem
* hospedagem barata

---

# Observações

Esse projeto foi feito com foco em simplicidade e praticidade para campanhas pequenas/médias.

Os dados são armazenados diretamente em arquivos JSON.

Ideal para:

* RPGs autorais
* fichas online
* ferramentas de mestre
* projetos indie
* protótipos rápidos

---

# Licença

Projeto pessoal.
