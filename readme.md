# CS-452 Data Engineering Assignments

This repository contains hands-on assignments for BYU CS-452 Data Engineering.

## Getting Started

### Prerequisites

1. **Docker Desktop** — [Download here](https://www.docker.com/products/docker-desktop/)
2. **Python 3.10+** — [Download here](https://www.python.org/downloads/)
3. **Git** — [Download here](https://git-scm.com/downloads)

### Setup (One-Time)

```bash
# Clone the repository
git clone https://github.com/byu-cs-452/codespace-assignments.git
cd codespace-assignments

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r semantic-search/requirements.txt
```

### Start the Database

```bash
cd semantic-search
docker compose up -d db
```

This starts a local PostgreSQL database with pgvector. First run pulls the image (~200MB).

### Verify Setup

```bash
python db_check.py
```

You should see: `✨ All checks passed! Your environment is ready.`

---

## Assignments

| Assignment | Folder | Description |
|------------|--------|-------------|
| Semantic Search | `semantic-search/` | Build a podcast recommender using pgvector |

---

## Alternative: TimescaleDB Cloud

If you can't install Docker, you can use [TimescaleDB](https://www.timescale.com/) cloud instead:

1. Create a free trial account at [timescale.com](https://www.timescale.com/)
2. Create a new service with **AI/ML** enabled (includes pgvector)
3. Update `utils.py` with your connection string
4. Skip the `docker compose` step

See `semantic-search/related_learning.md` for more details.

---

## Troubleshooting

### "Docker daemon not running"
Start Docker Desktop and wait for it to fully load.

### "Connection refused"
Make sure the database container is running:
```bash
docker compose up -d db
docker ps  # Should show 'vectordb' container
```

### Windows: psycopg2 won't install
Use the pre-built binary:
```bash
pip install psycopg2-binary
```

---

## Questions?

Post on the class discussion board or attend office hours.
