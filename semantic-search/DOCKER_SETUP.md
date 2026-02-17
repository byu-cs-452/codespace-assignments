# Docker Setup Guide

If you want to run PostgreSQL locally using Docker, follow this guide.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

## Steps

### 1. Start the Database

```bash
cd semantic-search
docker compose up -d db
```

This starts a PostgreSQL container with pgvector. First run downloads the image (~200MB).

**Wait 10-15 seconds for the database to be ready.** You can check status with:
```bash
docker ps
# You should see 'vectordb' container with status "healthy"
```

### 2. Get Your Connection String

Your connection string is:
```
postgresql://student:vector_lab_2024@localhost:5432/vectordb
```

### 3. Paste Into utils.py

Open `utils.py` and update the `CONNECTION` variable at the top:

```python
CONNECTION = "postgresql://student:vector_lab_2024@localhost:5432/vectordb"
```

### 4. Test It Works

```bash
python db_check.py
```

You should see: `✨ All checks passed! Your environment is ready.`

## Stopping the Database

When you're done:
```bash
docker compose down
```

To restart later:
```bash
docker compose up -d db
```

## Troubleshooting

### "Cannot connect to Docker daemon"
- Start Docker Desktop and wait for it to fully load
- Check: `docker ps`

### "Connection refused"
- Make sure container is running: `docker ps`
- Wait longer for it to be healthy
- View logs: `docker compose logs db`

### "Database is not healthy"
```bash
docker compose down
docker compose up -d db
# Wait 20 seconds
docker ps
```

### Want to reset the database?
```bash
docker compose down
docker volume rm semantic-search_postgres_data
docker compose up -d db
```
