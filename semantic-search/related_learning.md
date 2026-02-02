# Related Learning: How This Environment Works

This document explains how this development environment was created and the technologies behind it. **Understanding these concepts is valuable for your career**—you'll encounter them when building production systems or managing your own infrastructure.

## Table of Contents
- [How Docker Compose Works](#how-docker-compose-works)
- [What You're Learning](#what-youre-learning)
- [Alternative: TimescaleDB Cloud](#alternative-timescaledb-cloud)
- [Technologies Worth Learning](#technologies-worth-learning)
- [Further Reading](#further-reading)

---

## How Docker Compose Works

When you run `docker compose up -d db`, Docker creates a containerized PostgreSQL database with pgvector pre-installed.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Machine                              │
│                                                              │
│   ┌─────────────────────┐    ┌─────────────────────────────┐│
│   │  Python Environment │    │    Docker Container         ││
│   │                     │    │                             ││
│   │  • Your code        │◄──►│  • PostgreSQL 16            ││
│   │  • psycopg2         │    │  • pgvector extension       ││
│   │  • pandas           │    │  • vectordb database        ││
│   │                     │    │                             ││
│   └─────────────────────┘    └─────────────────────────────┘│
│                localhost:5432                                │
└─────────────────────────────────────────────────────────────┘
```

### docker-compose.yml Explained

```yaml
services:
  db:
    image: pgvector/pgvector:pg16    # PostgreSQL with pgvector pre-installed
    environment:
      POSTGRES_DB: vectordb           # Database name
      POSTGRES_USER: student          # Username
      POSTGRES_PASSWORD: vector_lab_2024
    ports:
      - "5432:5432"                   # Expose to localhost
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data
```

**Key concepts:**
- **Containers**: Isolated environments that package software with its dependencies
- **Volumes**: Persistent storage that survives container restarts
- **Port mapping**: Makes the container's port 5432 available on your machine

---

## What You're Learning

By running Docker locally, you're gaining real-world skills:

### 1. Container Basics
- Starting/stopping containers: `docker compose up -d` / `docker compose down`
- Viewing running containers: `docker ps`
- Viewing logs: `docker compose logs db`

### 2. Database Management
- Connecting to PostgreSQL from Python
- Using extensions like pgvector
- Writing efficient bulk inserts

### 3. Python Environment Management
- Virtual environments: `python -m venv .venv`
- Dependency management: `pip install -r requirements.txt`
- Isolation between projects

---

## Alternative: TimescaleDB Cloud

If you can't install Docker, you can use a managed database instead.

### Setting Up TimescaleDB

1. Go to [timescale.com](https://www.timescale.com/) and create a free trial account
2. Create a new service and select **AI/ML** (includes pgvector)
3. Navigate through the setup wizard—pay attention to:
   - Region selection
   - Instance configuration
   - Connection security settings
4. Copy your connection string from the dashboard
5. Update `utils.py` to use your connection string

**What you'll learn:**
- How database-as-a-service platforms work
- Managing connection strings and credentials
- Navigating cloud provider dashboards

### Other Cloud Options (For Reference)

These providers have smaller free tiers (our dataset is ~550MB):

| Service | Free Tier | pgvector | Notes |
|---------|-----------|----------|-------|
| [Neon](https://neon.tech/) | 512MB forever | ✅ Yes | Great for smaller datasets |
| [Supabase](https://supabase.com/) | 500MB forever | ✅ Yes | Full backend platform |

---

## Technologies Worth Learning

### Python Environment Management

#### uv — The Fast Python Package Manager

[uv](https://github.com/astral-sh/uv) is a blazing-fast Python package manager written in Rust:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Use uv instead of pip
uv venv                              # Create virtual environment
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
- **Docker Swarm**: Simpler alternative to Kubernetes

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

### Docker & Containers
- [Docker Getting Started](https://docs.docker.com/get-started/) — Official tutorial
- [Docker Compose Documentation](https://docs.docker.com/compose/) — Multi-container apps
- [Docker Hub](https://hub.docker.com/) — Find pre-built images

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
