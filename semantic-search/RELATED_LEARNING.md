# Related Learning: How This Codespace Works

This document explains how the GitHub Codespace environment was created, the value it provides, and how you could set up a similar environment locally if you prefer.

## Table of Contents
- [Why Codespaces for This Assignment?](#why-codespaces-for-this-assignment)
- [What's Inside This Codespace](#whats-inside-this-codespace)
- [How the Codespace Was Built](#how-the-codespace-was-built)
- [Running Locally (Alternative)](#running-locally-alternative)
- [Further Reading](#further-reading)

---

## Why Codespaces for This Assignment?

The traditional approach for this assignment required students to:

1. ❌ Sign up for a **TimescaleDB trial account** (30-day limit)
2. ❌ Configure **connection strings** and manage credentials
3. ❌ Set up a **local Python environment** with conda or venv
4. ❌ Deal with **network latency** when loading 800k rows over the internet
5. ❌ Troubleshoot **OS-specific issues** (Windows vs Mac vs Linux)

**With Codespaces, you get:**

| Benefit | Description |
|---------|-------------|
| 🚀 **One-Click Setup** | Fork → Open Codespace → Start coding |
| 🗄️ **Local PostgreSQL** | Database runs in the same container—blazing fast! |
| ⚡ **Fast Data Loading** | 800k rows load in seconds (same network, no internet latency) |
| 🐍 **Pre-configured Python** | Virtual environment with all dependencies ready |
| 🔧 **Consistent Environment** | Everyone has the same setup, fewer "works on my machine" issues |
| 💰 **Free for Students** | 60-180 hours/month depending on your plan |

### Performance Comparison

| Operation | TimescaleDB (cloud) | Codespace (local) |
|-----------|---------------------|-------------------|
| Insert 800k rows | 5-15 minutes | 10-30 seconds |
| Query latency | 50-200ms | <5ms |
| Connection setup | Manual credentials | Automatic |

---

## What's Inside This Codespace

When you create a Codespace from this repo, you get:

### 1. Docker Containers

```
┌─────────────────────────────────────────────────────────┐
│                    GitHub Codespace                      │
│  ┌───────────────────┐    ┌───────────────────────────┐ │
│  │   app container   │    │      db container         │ │
│  │                   │    │                           │ │
│  │  • Python 3.11    │◄──►│  • PostgreSQL 16          │ │
│  │  • VS Code Server │    │  • pgvector extension     │ │
│  │  • Your code      │    │  • vectordb database      │ │
│  │                   │    │                           │ │
│  └───────────────────┘    └───────────────────────────┘ │
│           localhost:5432 (internal network)              │
└─────────────────────────────────────────────────────────┘
```

### 2. Pre-installed VS Code Extensions
- **Python**: Full language support, debugging, linting
- **Pylance**: Advanced type checking and IntelliSense
- **SQLTools**: Browse and query the database visually
- **Jupyter**: Run notebooks if you prefer that workflow

### 3. Database Configuration
- **PostgreSQL 16** with **pgvector** extension
- Pre-created database: `vectordb`
- User: `student` / Password: `vector_lab_2024`
- Port: `5432` (forwarded automatically)

---

## How the Codespace Was Built

The Codespace is defined by two key files:

### `.devcontainer/devcontainer.json`

This tells GitHub how to configure the development environment:

```json
{
  "name": "CS-452 Semantic Search Environment",
  "dockerComposeFile": "../semantic-search/docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python", "mtxr.sqltools", ...]
    }
  },
  "postCreateCommand": "python3 -m venv .venv && pip install -r requirements.txt"
}
```

### `semantic-search/docker-compose.yml`

This defines the containers:

```yaml
services:
  db:
    image: pgvector/pgvector:pg16    # PostgreSQL with pgvector
    environment:
      POSTGRES_DB: vectordb
      POSTGRES_USER: student
      POSTGRES_PASSWORD: vector_lab_2024
      
  app:
    image: mcr.microsoft.com/devcontainers/python:3.11
    depends_on: [db]
```

### Key Design Decisions

1. **pgvector/pgvector:pg16 image**: Pre-built PostgreSQL with vector support
2. **Health checks**: App container waits for DB to be ready
3. **Persistent volume**: Database data survives container restarts
4. **Environment variables**: Connection info passed automatically

---

## Running Locally (Alternative)

If you prefer to run this assignment on your own machine, here are your options:

### Option 1: Local Docker (Recommended for Local)

If you have Docker Desktop installed:

```bash
# Clone the repo
git clone https://github.com/byu-cs-452/codespace-assignments.git
cd codespace-assignments/semantic-search

# Start PostgreSQL with pgvector
docker compose up -d db

# Create Python environment
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Download data and run
./download_data.sh
python db_check.py
```

### Option 2: Managed Database (TimescaleDB/Neon)

If you don't want to run Docker locally, you can use a managed PostgreSQL service:

#### TimescaleDB (30-day free trial)
1. Sign up at [timescale.com](https://www.timescale.com/)
2. Create a new service with **AI/ML** enabled (includes pgvector)
3. Copy your connection string
4. Update `utils.py` to use your connection string

#### Neon (Free tier with 512MB storage)
1. Sign up at [neon.tech](https://neon.tech/)
2. Create a project and enable pgvector extension
3. Use their connection string

⚠️ **Note**: Cloud databases will be slower for bulk inserts due to network latency.

### Option 3: Using UV for Python Management

[uv](https://github.com/astral-sh/uv) is a blazing-fast Python package manager written in Rust. It's a great alternative to pip/venv for local development:

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install uv (Windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Create environment and install dependencies
cd semantic-search
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -r requirements.txt
```

**Why UV?**
- 10-100x faster than pip
- Built-in virtual environment management
- Compatible with existing `requirements.txt` files
- Great for larger projects with many dependencies

### Option 4: Conda Environment

If you use Anaconda/Miniconda:

```bash
# Create environment
conda create -n cs452-semantic python=3.11
conda activate cs452-semantic

# Install dependencies
pip install -r requirements.txt

# For PostgreSQL client support
conda install -c conda-forge psycopg2
```

---

## Cloud Database Comparison

If you choose to use a managed database instead of the Codespace's local PostgreSQL:

| Service | Free Tier | pgvector | Notes |
|---------|-----------|----------|-------|
| [TimescaleDB](https://www.timescale.com/) | 30 days | ✅ Yes | Select "AI/ML" service type |
| [Neon](https://neon.tech/) | 512MB forever | ✅ Yes | Run `CREATE EXTENSION vector;` |
| [Supabase](https://supabase.com/) | 500MB forever | ✅ Yes | Great dashboard |
| [Railway](https://railway.app/) | $5 credit | ✅ Manual | Deploy pgvector image |
| [Render](https://render.com/) | 90 days | ❌ No | Standard Postgres only |

---

## Further Reading

### pgvector & Vector Databases
- [pgvector GitHub](https://github.com/pgvector/pgvector) - Official documentation
- [Intro to Vector Databases](https://www.pinecone.io/learn/vector-database/) - Pinecone's guide
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) - How embeddings work

### GitHub Codespaces
- [Codespaces Documentation](https://docs.github.com/en/codespaces)
- [Dev Containers Specification](https://containers.dev/)
- [Codespaces for Education](https://github.blog/2022-10-19-introducing-github-global-campus-and-codespaces-for-teachers/)

### Python Environment Management
- [uv Documentation](https://github.com/astral-sh/uv) - Fast Python package manager
- [Poetry](https://python-poetry.org/) - Dependency management tool
- [pyenv](https://github.com/pyenv/pyenv) - Python version management

### PostgreSQL & Data Engineering
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Usage](https://www.psycopg.org/docs/usage.html)
- [COPY Command for Fast Inserts](https://www.postgresql.org/docs/current/sql-copy.html)

---

## Questions?

If you have questions about the environment setup or want to learn more about DevOps and infrastructure, feel free to ask in the class discussion board or during office hours!
