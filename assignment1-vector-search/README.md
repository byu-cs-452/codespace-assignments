# Assignment 1: Vector Search with pgvector

## Overview

In this assignment, you'll learn to:
- Perform ETL (Extract, Transform, Load) on a 500MB dataset
- Store data in a Postgres database with pgvector extension
- Implement semantic search using vector embeddings

## Prerequisites

- GitHub account with access to this repository
- GitHub Codespaces (free tier available with Student Developer Pack)

## Getting Started

### 1. Fork and Open in Codespace

1. **Fork this repository** to your GitHub account
2. Click the green **"Code"** button
3. Select **"Codespaces"** tab
4. Click **"Create codespace on main"**

The environment will automatically:
- ✅ Spin up a Postgres database with pgvector
- ✅ Create a Python virtual environment
- ✅ Install all required packages
- ✅ Run a sanity check to verify everything works

**First-time setup takes ~2-3 minutes.** You'll see the setup progress in the terminal.

### 2. Verify Your Setup

After the Codespace finishes building, you should see:

```
✨ All checks passed! Your environment is ready for Assignment 1.
```

If you need to manually verify, activate the virtual environment and run the check:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run sanity check
python assignment1-vector-search/db_check.py
```

### 3. Working with Jupyter Notebooks

This environment supports **Jupyter notebooks** for a Colab-like experience:

1. Create a new file with `.ipynb` extension
2. VS Code will automatically recognize it as a Jupyter notebook
3. Select the Python interpreter: `.venv/bin/python`
4. Start coding cell-by-cell!

**Example first cell:**
```python
import psycopg2
import pandas as pd
from pgvector.psycopg2 import register_vector

# Connect to database
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='vectordb',
    user='student',
    password='vector_lab_2024'
)
print("✅ Connected to database!")
```

## Database Connection Details

- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `vectordb`
- **Username**: `student`
- **Password**: `vector_lab_2024`

## Assignment Tasks

### Task 1: Data Loading
- Download the provided dataset (link on Canvas)
- Load it into a Pandas DataFrame
- Explore the data structure

### Task 2: Database Schema
- Design a table schema for the dataset
- Create the table in Postgres
- Include a vector column for embeddings

### Task 3: ETL Pipeline
- Transform the data as needed
- Generate vector embeddings (we'll provide the model)
- Load data into your Postgres table

### Task 4: Semantic Search
- Implement a function to search by vector similarity
- Test with sample queries
- Analyze and report your results

## Troubleshooting

### Database won't connect
```bash
# Check if database is running
docker ps

# Rebuild the container
# Cmd/Ctrl + Shift + P → "Rebuild Container"
```

### Virtual environment issues
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r assignment1-vector-search/requirements.txt
```

### Package installation fails
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r assignment1-vector-search/requirements.txt
```

## Submission

1. Complete all tasks in a Jupyter notebook named `assignment1_solution.ipynb`
2. Commit and push your work to your forked repository
3. Submit the link to your repository on Canvas

## Resources

- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Postgres Documentation](https://www.postgresql.org/docs/)
- [GitHub Codespaces Docs](https://docs.github.com/en/codespaces)

## Questions?

Post on the class discussion board or attend office hours.

---

**Happy coding! 🚀**
