# 🎓 SynCampus - Portal Acadêmico

Um sistema completo de gestão acadêmica para gerenciar alunos, disciplinas, matrículas, notas e relatórios em uma instituição educacional.

---

## 📚 Visão Geral

**SynCampus** é uma plataforma web que permite:

- **Alunos**: Visualizar suas disciplinas, matrículas, notas e média geral
- **Professores**: Lançar notas, visualizar seus alunos e disciplinas
- **Administradores**: Gerenciar alunos, disciplinas, matrículas e notas do sistema

O sistema foi desenvolvido com **FastAPI** (backend) e **Streamlit** (frontend), garantindo uma arquitetura moderna e escalável.

---

## 🏗️ Arquitetura

```
Frontend (Streamlit)              Backend (FastAPI)                 Database
┌─────────────────────┐          ┌──────────────────┐              ┌────────┐
│  Portal do Aluno    │          │  /auth           │              │ SQLite │
│  Portal Professor   │  ◄───►   │  /alunos         │  ◄────────►  │  ou    │
│  Painel Admin       │          │  /disciplinas    │              │ MySQL  │
└─────────────────────┘          │  /matriculas     │              │        │
                                 │  /notas          │              └────────┘
                                 │  /relatorios     │
                                 └──────────────────┘
```

---

## 🎯 Funcionalidades

### 👤 Para Alunos
- ✅ Visualizar perfil pessoal
- ✅ Ver disciplinas cadastradas
- ✅ Acompanhar matrículas com status
- ✅ Consultar notas lançadas pelo professor
- ✅ Visualizar média geral

### 👨‍🏫 Para Professores
- ✅ Ver disciplinas que leciona
- ✅ Visualizar alunos matriculados
- ✅ Lançar/editar notas para alunos
- ✅ Acompanhar matrículas e notas

### 🛡️ Para Administradores
- ✅ Gerenciar alunos (CRUD)
- ✅ Gerenciar disciplinas (CRUD)
- ✅ Gerenciar matrículas (CRUD)
- ✅ Gerenciar notas (CRUD)
- ✅ Dashboard com estatísticas

---

## 📋 Pré-requisitos

- **Python 3.8+** 
- **pip** (gerenciador de pacotes Python)
- **Git**

---

## 🚀 Como Rodar o Projeto

### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/higorjulio/APS.git
cd APS
```

### 2️⃣ Configure o Backend

```bash
cd backend

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o servidor FastAPI
uvicorn app.main:app --reload
```

O backend estará disponível em: **http://127.0.0.1:8000**

### 3️⃣ Configure o Frontend

Em outro terminal:

```bash
cd frontend

# Instale as dependências
pip install -r requirements.txt

# Inicie o Streamlit
streamlit run app.py
```

O frontend estará disponível em: **http://localhost:8501**

---

## 📂 Estrutura do Projeto

```
APS/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth.py           # Autenticação e login
│   │   │   ├── students.py       # Gestão de alunos
│   │   │   ├── disciplines.py    # Gestão de disciplinas
│   │   │   ├── enrollments.py    # Gestão de matrículas
│   │   │   ├── grades.py         # Gestão de notas
│   │   │   └── reports.py        # Relatórios
│   │   ├── auth.py               # Segurança JWT
│   │   ├── database.py           # Conexão com banco
│   │   ├── models.py             # Modelos de dados
│   │   ├── schemas.py            # Schemas Pydantic
│   │   └── main.py               # Aplicação principal
│   └── requirements.txt
│
├── frontend/
│   ├── api.py                    # Cliente HTTP para API
│   ├── app.py                    # Página de login
│   ├── pages/
│   │   ├── admin.py              # Painel administrativo
│   │   ├── aluno.py              # Portal do aluno
│   │   └── professor.py          # Portal do professor
│   └── requirements.txt
│
└── README.md
```

---

## 🔐 Autenticação

O sistema usa **JWT (JSON Web Tokens)** para autenticação segura.

### Fluxo de Login:
1. Usuário insere email e senha
2. Sistema valida credenciais no banco de dados
3. Se válido, retorna um token JWT
4. Token é armazenado na sessão Streamlit
5. Token é enviado em todas as requisições (header `Authorization: Bearer {token}`)

### Permissões por Papel:

| Recurso | Admin | Professor | Aluno |
|---------|-------|-----------|-------|
| Ver alunos | ✅ | ✅ | ❌ |
| Lançar notas | ✅ | ✅ | ❌ |
| Ver notas | ✅ | ✅ | ✅ |
| Gerenciar disciplinas | ✅ | ❌ | ❌ |
| Gerenciar matrículas | ✅ | ❌ | ❌ |

---

## 📡 Endpoints da API

### 🔓 Autenticação (sem token)
```
POST   /auth/register              # Criar nova conta
POST   /auth/login                 # Fazer login
```

### 🔒 Alunos (requer autenticação)
```
GET    /alunos/                    # Listar todos os alunos (admin/prof)
GET    /alunos/{id}                # Obter aluno específico
POST   /alunos/                    # Criar novo aluno (admin)
PUT    /alunos/{id}                # Atualizar aluno (admin)
DELETE /alunos/{id}                # Deletar aluno (admin)
GET    /alunos/buscar?q=...        # Buscar aluno por matrícula/curso
```

### 📚 Disciplinas
```
GET    /disciplinas/               # Listar disciplinas
POST   /disciplinas/               # Criar disciplina (admin)
PUT    /disciplinas/{id}           # Atualizar disciplina (admin)
DELETE /disciplinas/{id}           # Deletar disciplina (admin)
GET    /disciplinas/buscar?q=...   # Buscar disciplina
```

### 📝 Matrículas
```
GET    /matriculas/                # Listar matrículas
POST   /matriculas/                # Criar matrícula (admin)
GET    /matriculas/aluno/{id}      # Matrículas de um aluno
PUT    /matriculas/{id}/status     # Atualizar status (admin/prof)
DELETE /matriculas/{id}            # Deletar matrícula (admin)
```

### ⭐ Notas
```
GET    /notas/                     # Listar notas (suas ou todas)
POST   /notas/                     # Lançar nota (admin/prof)
GET    /notas/matricula/{id}       # Notas de uma matrícula
PUT    /notas/{id}                 # Editar nota (admin/prof)
DELETE /notas/{id}                 # Deletar nota (admin)
```

### 📊 Relatórios
```
GET    /relatorios/aluno/{id}      # Relatório do aluno
```

---

## 👥 Contas de Teste

Ao registrar uma conta, escolha o tipo de usuário:

```
Email: aluno@example.com
Senha: senha123
Tipo: aluno

Email: professor@example.com
Senha: senha123
Tipo: professor

Email: admin@example.com
Senha: senha123
Tipo: admin
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web rápido e moderno
- **SQLAlchemy** - ORM para banco de dados
- **Pydantic** - Validação de dados
- **Python-Jose** - Implementação de JWT
- **Passlib** - Hash de senhas seguro

### Frontend
- **Streamlit** - Framework para interface web
- **Requests** - Cliente HTTP
- **Python** - Linguagem de programação

### Banco de Dados
- **SQLite** (desenvolvimento) ou **MySQL** (produção)

---

## 📖 Como Usar

### 🎓 Portal do Aluno

1. Acesse a aplicação em `http://localhost:8501`
2. Clique em "Criar Conta" e registre-se como **aluno**
3. Faça login com sua conta
4. Explore as abas:
   - **Disciplinas**: Veja as disciplinas cadastradas
   - **Matrículas**: Acompanhe suas matrículas com status e notas
   - **Notas**: Visualize todas as suas notas

### 👨‍🏫 Portal do Professor

1. Registre-se como **professor**
2. Faça login
3. Acesse o painel para:
   - Ver suas disciplinas
   - Visualizar alunos matriculados
   - Lançar notas para alunos

### 🛡️ Painel Administrativo

1. Registre-se como **admin**
2. Faça login
3. Gerencie todos os recursos:
   - Alunos
   - Disciplinas
   - Matrículas
   - Notas

---

## 🐛 Troubleshooting

### Erro: "Conexão recusada" ao conectar com backend
- Certifique-se de que o backend está rodando em `http://127.0.0.1:8000`
- Verifique se a porta 8000 não está em uso

### Erro: "Token inválido" no login
- Faça logout e login novamente
- Limpe o cache do navegador

### Erro: "Banco de dados não encontrado"
- Execute as migrações do banco (se houver)
- Certifique-se que o arquivo do banco foi criado

---

## 📝 Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend/`:

```
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=sqlite:///./app.db
# ou para MySQL:
# DATABASE_URL=mysql://user:password@localhost/syncampus
```

---

## 🤝 Contribuindo

Para contribuir com o projeto:

1. Faça um Fork
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto é de código aberto sob a licença MIT.

---

## 👨‍💻 Desenvolvedor

**Higor Julio** - [@higorjulio](https://github.com/higorjulio)

---

## 📞 Suporte

Para dúvidas ou sugestões, abra uma [issue](https://github.com/higorjulio/APS/issues) no repositório.

**Versão:** 1.0.0  
**Última atualização:** Maio 2026

### 2. Configure o Backend (FastAPI)

#### 2.1 Navegue até a pasta do backend
```bash
cd backend
```

#### 2.2 Crie um arquivo `.env` com as configurações do banco de dados
```bash
# Crie o arquivo backend/.env
# Adicione (ajuste com suas credenciais):
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/sincampus
```

#### 2.3 Crie um ambiente virtual Python
```bash
# No Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate

# No macOS/Linux:
python3 -m venv venv
source venv/bin/activate
```

#### 2.4 Instale as dependências
```bash
pip install -r requirements.txt
```

#### 2.5 Rode o servidor backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em: **http://localhost:8000**

Documentação da API em: **http://localhost:8000/docs** (Swagger UI)

### 3. Configure o Frontend

#### 3.1 Navegue até a pasta do frontend
```bash
cd frontend
```

#### 3.2 Instale as dependências
```bash
npm install
```

#### 3.3 Configure as variáveis de ambiente
```bash
# Crie o arquivo frontend/.env.local
# Adicione:
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 3.4 Rode o servidor frontend
```bash
npm run dev
```

O frontend estará disponível em: **http://localhost:3000**

## 📁 Estrutura do Projeto

```
APS/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Aplicação principal
│   │   ├── database.py     # Configuração do banco de dados
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── schemas.py      # Schemas Pydantic
│   │   ├── auth.py         # Autenticação
│   │   └── routes/         # Rotas da API
│   │       ├── auth.py
│   │       ├── students.py
│   │       ├── disciplines.py
│   │       ├── enrollments.py
│   │       ├── grades.py
│   │       └── reports.py
│   └── requirements.txt     # Dependências Python
├── frontend/               # Aplicação Next.js/React
│   └── pages/
├── tests/                  # Testes do projeto
│   └── jmeter/
└── README.md
```

## 🔑 Variáveis de Ambiente

### Backend (`.env`)
```
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/sincampus
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🗄️ Banco de Dados

O projeto usa **MySQL**. Antes de rodar pela primeira vez:

1. Crie o banco de dados:
```sql
CREATE DATABASE sincampus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. As tabelas serão criadas automaticamente quando você rodar o backend pela primeira vez.

## 🧪 Testes

### Testes de Performance com JMeter
```bash
# Execute os testes localizados em tests/jmeter/
jmeter -t tests/jmeter/seu_teste.jmx
```

## 📚 API Endpoints Principais

A documentação interativa da API está disponível em: **http://localhost:8000/docs**

Alguns endpoints principais:
- `POST /auth/login` - Fazer login
- `GET /students` - Listar estudantes
- `GET /disciplines` - Listar disciplinas
- `POST /enrollments` - Criar matrícula
- `GET /grades` - Listar notas

## ⚠️ Possíveis Problemas

### Backend não conecta ao MySQL
- Verifique se o MySQL está rodando
- Confirme as credenciais no arquivo `.env`
- Verifique se o banco de dados foi criado

### Frontend não conecta ao backend
- Verifique se o backend está rodando em `http://localhost:8000`
- Confirme a URL em `frontend/.env.local`
- Verifique o console do navegador para erros de CORS

### Porta já está em uso
- **Backend**: `lsof -i :8000` (Mac/Linux) ou `netstat -ano | findstr :8000` (Windows)
- **Frontend**: `lsof -i :3000` (Mac/Linux) ou `netstat -ano | findstr :3000` (Windows)

## 👥 Contribuindo

1. Crie uma branch: `git checkout -b feature/sua-funcionalidade`
2. Faça suas mudanças e commit: `git commit -am 'Adiciona nova funcionalidade'`
3. Push para a branch: `git push origin feature/sua-funcionalidade`
4. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT.

---

**Dúvidas?** Abra uma issue ou entre em contato com os desenvolvedores.
