# Related Learning: How This Codespace Works

This document explains how this GitHub Codespace environment was created and the technologies behind it. While we've simplified the setup for this assignment, **understanding these concepts is valuable for your career**—you may encounter them when building production systems or managing your own infrastructure.

> 💡 **A Note from Your Instructor**: By using Codespaces, we've removed some "real-world" setup steps (creating cloud database accounts, managing connection strings, etc.). While this lets you focus on the core learning objectives, those skills *are* valuable. This document is here so you can still learn about what we've abstracted away—and explore these technologies on your own when you're ready.

## Table of Contents
- [What This Codespace Provides](#what-this-codespace-provides)
- [How the Codespace Was Built](#how-the-codespace-was-built)
- [What You're Missing (And Why It Matters)](#what-youre-missing-and-why-it-matters)
- [Running Locally (The "Harder" Way)](#running-locally-the-harder-way)
- [Technologies Worth Learning](#technologies-worth-learning)
- [Further Reading](#further-reading)

---

## What This Codespace Provides

When you create a Codespace from this repo, you get a fully configured environment:

### Architecture

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

### What's Pre-Configured

| Component | What You Get |
|-----------|--------------|
| **PostgreSQL 16** | Database server with pgvector extension already installed |
| **Python 3.11** | Virtual environment with all dependencies |
| **VS Code Extensions** | Python, SQLTools (browse your database visually), Jupyter |
| **Connection strings** | Automatically configured via environment variables |

---

## How the Codespace Was Built

The Codespace is defined by two configuration files. Understanding these is useful if you ever need to create reproducible development environments for your own projects or teams.

### `.devcontainer/devcontainer.json`

This file tells GitHub (and VS Code) how to configure the development container:

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

**Key concepts:**
- **Dev Containers**: A specification for defining development environments as code
- **postCreateCommand**: Runs once when the container is first created
- **Extensions**: Automatically installed so everyone has the same tools

### `semantic-search/docker-compose.yml`

This defines the containers that run together:

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

**Key concepts:**
- **Docker Compose**: Orchestrates multiple containers that work together
- **Health checks**: The app container waits for the database to be ready
- **Volumes**: Database data persists even if containers restart

---

## What You're Missing (And Why It Matters)

By using this Codespace, you skip several steps that are common in real-world development:

### 1. Setting Up a Cloud Database

In production, you'd typically:
- **Choose a provider** (AWS RDS, Google Cloud SQL, TimescaleDB, Neon, Supabase)
- **Configure instance size**, storage, backups, and security
- **Manage connection strings** and secrets securely
- **Set up networking** (VPCs, firewall rules, SSL certificates)

**Why it matters**: Understanding database-as-a-service offerings is essential for most software engineering roles.

### 2. Managing Python Environments

We create the virtual environment for you, but in practice you'd need to:
- **Choose a tool**: venv, conda, poetry, or uv
- **Pin dependency versions** for reproducibility
- **Handle conflicts** between packages
- **Set up CI/CD** to test with consistent environments

**Why it matters**: Environment management is a common source of bugs ("works on my machine").

### 3. Configuring Connection Strings

We hardcode the connection details. In production:
- **Secrets are stored securely** (environment variables, secret managers)
- **Different environments** (dev, staging, prod) have different credentials
- **Connection pooling** is used for performance

**Why it matters**: Credential management is a critical security skill.

---

## Running Locally (The "Harder" Way)

If you want to experience the full setup process—which we encourage!—here are your options:

### Option 1: Local Docker

Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and run:

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

# Run the assignment
./download_data.sh
python db_check.py
```

This gives you the same setup as the Codespace, but running on your machine.

### Option 2: Cloud Database (Real-World Experience)

Try setting up a managed database service. This is valuable hands-on experience:

#### TimescaleDB
1. Go to [timescale.com](https://www.timescale.com/) and create a free trial account
2. Create a new service with **AI/ML** enabled (includes pgvector)
3. Navigate through the setup wizard and note the connection details
4. Update your code to use the connection string they provide

#### Neon (Free Tier)
1. Sign up at [neon.tech](https://neon.tech/)
2. Create a project (free tier includes 512MB storage)
3. Run `CREATE EXTENSION vector;` to enable pgvector
4. Use their connection string in your code

#### Supabase (Free Tier)
1. Sign up at [supabase.com](https://supabase.com/)
2. Create a project (free tier includes 500MB)
3. pgvector is pre-installed; enable it in the SQL editor
4. Find connection details in Settings → Database

### Cloud Database Comparison

| Service | Free Tier | pgvector | Good For |
|---------|-----------|----------|----------|
| [TimescaleDB](https://www.timescale.com/) | 30 days trial | ✅ Built-in | Time-series + vectors |
| [Neon](https://neon.tech/) | 512MB forever | ✅ Yes | Serverless, branching |
| [Supabase](https://supabase.com/) | 500MB forever | ✅ Yes | Full backend platform |
| [Railway](https://railway.app/) | $5 credit | ⚠️ Manual | Quick deployments |

---

## Technologies Worth Learning

These tools are worth exploring for your career:

### Python Environment Management

#### uv — The Fast Python Package Manager

[uv](https://github.com/astral-sh/uv) is a blazing-fast Python package manager written in Rust. It's becoming increasingly popular:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Use uv instead of pip
uv venv                          # Create virtual environment
uv pip install -r requirements.txt   # Install packages (very fast!)
```

**Why learn it**: Modern Python development is moving toward faster, Rust-based tools.

#### Poetry — Dependency Management

[Poetry](https://python-poetry.org/) handles dependencies and packaging:

```bash
poetry init              # Create pyproject.toml
poetry add pandas        # Add a dependency
poetry install           # Install all dependencies
poetry shell             # Activate environment
```

**Why learn it**: Industry standard for Python projects that need reproducible builds.

### Container Orchestration

- **Docker Compose**: What we use here—good for development and small deployments
- **Kubernetes**: Industry standard for production container orchestration
- **Dev Containers**: The standard we use for Codespaces—works in VS Code too

### Database Technologies

- **pgvector**: The extension we use for vector similarity search
- **PostgreSQL**: The world's most advanced open-source database
- **Vector databases**: Purpose-built alternatives like Pinecone, Weaviate, Qdrant

---

## Further Reading

### Vector Databases & Embeddings
- [pgvector GitHub](https://github.com/pgvector/pgvector) — How pgvector works
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings) — Creating embeddings
- [Vector Database Comparison](https://www.pinecone.io/learn/vector-database/) — When to use what

### Development Environments
- [Dev Containers Specification](https://containers.dev/) — The standard we use
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces) — Deep dive into Codespaces
- [Docker Compose Docs](https://docs.docker.com/compose/) — Container orchestration

### Python Tools
- [uv Documentation](https://github.com/astral-sh/uv) — Fast package management
- [Poetry Documentation](https://python-poetry.org/docs/) — Modern dependency management
- [pyenv](https://github.com/pyenv/pyenv) — Python version management

### PostgreSQL
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — Learn PostgreSQL
- [psycopg2 Documentation](https://www.psycopg.org/docs/) — Python PostgreSQL adapter
- [COPY for Fast Inserts](https://www.postgresql.org/docs/current/sql-copy.html) — Bulk loading data

---

## Questions?

If you have questions about these technologies or want to discuss DevOps and infrastructure topics, feel free to ask in the class discussion board or during office hours. These skills are valuable for your career!
