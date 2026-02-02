# Semantic Search: Podcast Recommender System

Build a podcast recommender system using **pgvector** and semantic search! You'll work with the [Lex Fridman Podcast](https://www.youtube.com/lexfridman) dataset containing 346 podcasts and 832,839 transcript segments, each with pre-computed 128-dimensional embeddings.

## Learning Objectives

In this assignment, you'll learn to:
- Perform ETL (Extract, Transform, Load) on a 500MB dataset
- Store data in a Postgres database with pgvector extension
- Implement semantic search using vector embeddings

## Quick Start

### 1. Fork and Open in Codespace

1. **Fork this repository** to your GitHub account
2. Click the green **"Code"** button → **"Codespaces"** → **"Create codespace on main"**
3. Wait ~2-3 minutes for the environment to build

### 2. Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### 3. Download the Dataset

```bash
cd semantic-search
chmod +x download_data.sh
./download_data.sh
```

This downloads ~500MB of podcast data and embeddings from Google Drive.

### 4. Verify Database Connection

```bash
python db_check.py
```

You should see: `✨ All checks passed! Your environment is ready.`

## Assignment Tasks

Complete the TODO sections in each file:

### Step 1: `db_build.py` - Create Tables

Write SQL statements to create:
- `podcast` table (id, title)
- `segment` table (id, start_time, end_time, content, embedding, podcast_id)

```bash
python db_build.py
```

### Step 2: `db_insert.py` - Load Data

- Read embeddings from `embedding.jsonl` files
- Read podcast text from `batch_request_XX.jsonl` files
- Insert data into PostgreSQL using `fast_pg_insert()`

```bash
python db_insert.py
```

### Step 3: `db_query.py` - Semantic Search

Write queries to answer:

| Query | Description |
|-------|-------------|
| Q1 | 5 most **similar** segments to "267:476" (alien life) |
| Q2 | 5 most **dissimilar** segments to "267:476" |
| Q3 | 5 most similar segments to "48:511" (neural networks) |
| Q4 | 5 most similar segments to "51:56" (dark energy) |
| Q5 | 5 most similar **episodes** to segments a) 267:476, b) 48:511, c) 51:56 |
| Q6 | 5 most similar episodes to podcast "VeH7qKZr0WI" (Balaji) |

```bash
python db_query.py
```

## Database Schema

### `podcast` table
| Column | Type | Description |
|--------|------|-------------|
| id | TEXT (PK) | YouTube video ID (e.g., 'TRdL6ZzWBS0') |
| title | TEXT | Full podcast title |

### `segment` table
| Column | Type | Description |
|--------|------|-------------|
| id | TEXT (PK) | Format: "podcast_idx:segment_idx" (e.g., '89:115') |
| start_time | FLOAT | Start timestamp in seconds |
| end_time | FLOAT | End timestamp in seconds |
| content | TEXT | Transcribed text |
| embedding | VECTOR(128) | 128-dimensional embedding |
| podcast_id | TEXT (FK) | References podcast.id |

## pgvector Distance Functions

```sql
-- L2 (Euclidean) distance - USE THIS FOR ALL QUERIES
embedding <-> other_embedding

-- Other options (not used in this assignment):
embedding <#> other_embedding  -- negative inner product
embedding <=> other_embedding  -- cosine distance
embedding <+> other_embedding  -- L1 distance
```

## Data Files

After running `download_data.sh`, you'll have:

```
data/
├── batch_request_00.jsonl  # Podcast text + metadata
├── batch_request_01.jsonl
├── ...
├── embedding_00.jsonl      # 128-dim embeddings
├── embedding_01.jsonl
└── ...
```

### Sample `batch_request` document:
```json
{
  "custom_id": "89:115",
  "body": {
    "input": "have been possible without these approaches?",
    "metadata": {
      "title": "Podcast: Boris Sofman: Waymo...",
      "podcast_id": "U_AREIyd0Fc",
      "start_time": 484.52,
      "stop_time": 487.08
    }
  }
}
```

### Sample `embedding` document:
```json
{
  "custom_id": "89:115",
  "response": {
    "body": {
      "data": [{"embedding": [0.003, -0.012, ..., 0.045]}]
    }
  }
}
```

## Database Connection

The Codespace includes a local PostgreSQL instance with pgvector. Connection details:

| Property | Value |
|----------|-------|
| Host | `localhost` |
| Port | `5432` |
| Database | `vectordb` |
| Username | `student` |
| Password | `vector_lab_2024` |

The `utils.py` file provides helper functions to connect automatically.

## Files Overview

| File | Purpose |
|------|---------|
| `db_build.py` | Create database tables |
| `db_insert.py` | Load data into tables |
| `db_query.py` | Write semantic search queries |
| `utils.py` | Helper functions (provided) |
| `db_check.py` | Verify environment setup |
| `download_data.sh` | Download dataset from Google Drive |

## Deliverables

Submit a ZIP or PDF containing:
1. Your completed code files (`db_build.py`, `db_insert.py`, `db_query.py`)
2. A PDF with the queries and results for Q1-Q6

## Want to Learn More?

📚 **[related_learning.md](./related_learning.md)** — Curious how this Codespace was built? Want to run locally instead? This guide covers:

- How the Codespace environment was created
- Why local PostgreSQL is faster than cloud databases for this assignment
- Setting up locally with Docker, TimescaleDB, or Neon
- Using **uv** for fast Python environment management
- Links to pgvector, PostgreSQL, and DevOps resources

---

## Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Lex Fridman Podcast Dataset (HuggingFace)](https://huggingface.co/datasets/Whispering-GPT/lex-fridman-podcast)

## Troubleshooting

### "Data directory not found"
Run `./download_data.sh` to download the dataset.

### Database won't connect
```bash
# Check if containers are running
docker ps

# Rebuild if needed (Ctrl+Shift+P → "Rebuild Container")
```

### Virtual environment issues
```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

**Questions?** Post on the class discussion board or attend office hours.
