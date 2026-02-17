"""
Utility functions for the semantic search assignment.

To get started:
1. Follow DOCKER_SETUP.md or TIMESCALEDB_SETUP.md to get a connection string
2. Paste your connection string into the CONNECTION variable below
3. Run: python db_check.py
"""

import io
import pandas as pd
import psycopg2
from typing import List

# ============================================================================
# EDIT THIS: Paste your database connection string here
# ============================================================================
# Docker example:
#   postgresql://student:vector_lab_2024@localhost:5432/vectordb
#
# TimescaleDB example:
#   postgresql://user:password@xyz.timescale.cloud:5432/tsdb
#
CONNECTION = "postgresql://student:vector_lab_2024@localhost:5432/vectordb"


def get_connection_string() -> str:
    """Return the database connection string."""
    return CONNECTION


def get_connection() -> psycopg2.extensions.connection:
    """
    Create and return a database connection.
    """
    return psycopg2.connect(get_connection_string())


def fast_pg_insert(
    df: pd.DataFrame, 
    connection_string: str, 
    table_name: str, 
    columns: List[str]
) -> None:
    """
    Inserts data from a pandas DataFrame into a PostgreSQL table using 
    the COPY command for fast insertion.
    
    This is MUCH faster than row-by-row inserts for large datasets.
    For 800k rows, this takes seconds instead of hours.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the data to be inserted.
    connection_string : str
        The connection string to the PostgreSQL database.
    table_name : str
        The name of the target table in the PostgreSQL database.
    columns : List[str]
        A list of column names in the target table that correspond 
        to the DataFrame columns.

    Returns:
    --------
    None
    
    Example:
    --------
    >>> df = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
    >>> fast_pg_insert(df, CONNECTION, 'users', ['id', 'name'])
    """
    conn = psycopg2.connect(connection_string)
    _buffer = io.StringIO()
    df.to_csv(_buffer, sep=";", index=False, header=False)
    _buffer.seek(0)
    
    with conn.cursor() as c:
        c.copy_from(
            file=_buffer,
            table=table_name,
            sep=";",
            columns=columns,
            null=''
        )
    
    conn.commit()
    conn.close()
    print(f"✅ Inserted {len(df)} rows into {table_name}")


def vector_to_pg_format(vector: List[float]) -> str:
    """
    Convert a Python list of floats to PostgreSQL vector format.
    
    Parameters:
    -----------
    vector : List[float]
        A list of float values representing the embedding vector.
        
    Returns:
    --------
    str
        A string in PostgreSQL vector format: '[0.1,0.2,0.3,...]'
    
    Example:
    --------
    >>> vector_to_pg_format([0.1, 0.2, 0.3])
    '[0.1,0.2,0.3]'
    """
    return "[" + ",".join(str(x) for x in vector) + "]"
