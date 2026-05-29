# SynCampus - Sistema de Matrículas

Sistema web para gerenciamento de matrículas, disciplinas e notas de estudantes.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 14+** ([Download](https://nodejs.org/))
- **MySQL 8.0+** ou outro banco de dados SQL compatible ([Download](https://www.mysql.com/downloads/))

## 🚀 Como Rodar o Projeto

### 1. Clone o Repositório

```bash
git clone https://github.com/higorjulio/APS.git
cd APS
```

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
