"""
db_query.py - Write semantic search queries against the podcast database.

This script contains queries to find similar podcast segments and episodes
using pgvector's distance functions.

pgvector distance operators:
    <->  L2 (Euclidean) distance
    <#>  (negative) inner product  
    <=>  cosine distance
    <+>  L1 (Manhattan) distance

For this assignment, use L2 distance (<->) for all queries.

Run this script AFTER db_build.py and db_insert.py have been completed.

Usage:
    python db_query.py
"""

import psycopg2
from utils import get_connection_string

# Get database connection  
CONNECTION = get_connection_string()


# =============================================================================
# Helper function to run queries
# =============================================================================
def run_query(query: str, description: str):
    """Execute a query and print the results."""
    print(f"\n{'='*60}")
    print(f"📊 {description}")
    print('='*60)
    
    conn = psycopg2.connect(CONNECTION)
    cursor = conn.cursor()
    cursor.execute(query)
    
    results = cursor.fetchall()
    for i, row in enumerate(results, 1):
        print(f"\n{i}. {row}")
    
    cursor.close()
    conn.close()
    
    return results


# =============================================================================
# Q1: Five most SIMILAR segments to segment "267:476"
# =============================================================================
# Input text: "that if we were to meet alien life at some point"
#
# TODO: Write a query that:
# - Finds the embedding for segment "267:476"
# - Calculates L2 distance to all other segments
# - Returns the 5 closest segments (EXCLUDING the query segment itself)
# - For each result, return:
#     - podcast title (from podcast table)
#     - segment id
#     - segment content (raw text)
#     - start_time
#     - end_time (note: it's called 'end_time' in our schema, 'stop_time' in the original)
#     - embedding distance

Q1_SIMILAR = """

"""


# =============================================================================
# Q2: Five most DISSIMILAR segments to segment "267:476"
# =============================================================================
# Input text: "that if we were to meet alien life at some point"
#
# TODO: Same as Q1, but find the FURTHEST segments instead
# Hint: Order by distance DESC instead of ASC

Q2_DISSIMILAR = """

"""


# =============================================================================
# Q3: Five most similar segments to segment "48:511"
# =============================================================================
# Input: "Is it is there something especially interesting and profound 
#         to you in terms of our current deep learning neural network, 
#         artificial neural network approaches and the whatever we do 
#         understand about the biological neural network."
#
# TODO: Same structure as Q1, different segment ID

Q3_NEURAL = """

"""


# =============================================================================
# Q4: Five most similar segments to segment "51:56"
# =============================================================================
# Input: "But what about like the fundamental physics of dark energy? 
#         Is there any understanding of what the heck it is?"
#
# TODO: Same structure as Q1, different segment ID

Q4_PHYSICS = """

"""


# =============================================================================
# Q5: Five most similar EPISODES to given segments
# =============================================================================
# For each segment, find the 5 most similar podcast EPISODES (not segments).
#
# Hint: You can represent an episode's embedding as the AVERAGE of all its
#       segment embeddings. Use PostgreSQL's AVG() function on the vector.
#
# a) Segment "267:476"
# b) Segment "48:511"  
# c) Segment "51:56"
#
# For each result, return:
#   - Podcast title
#   - Embedding distance

Q5A_EPISODE = """

"""

Q5B_EPISODE = """

"""

Q5C_EPISODE = """

"""


# =============================================================================
# Q6: Five most similar episodes to podcast "VeH7qKZr0WI"
# =============================================================================
# Input Episode: "Balaji Srinivasan: How to Fix Government, Twitter, 
#                 Science, and the FDA | Lex Fridman Podcast #331"
#
# TODO: Find the 5 most similar podcast episodes to this one.
# Hint: Use the same averaging approach as Q5
#
# For each result, return:
#   - Podcast title
#   - Embedding distance

Q6_BALAJI = """

"""


# =============================================================================
# Main execution
# =============================================================================
def main():
    print("🔍 Running semantic search queries...")
    
    # Q1: Similar to alien life segment
    if Q1_SIMILAR.strip():
        run_query(Q1_SIMILAR, "Q1: 5 most similar segments to '267:476' (alien life)")
    else:
        print("\n⚠️  Q1: Not implemented yet")
    
    # Q2: Dissimilar to alien life segment
    if Q2_DISSIMILAR.strip():
        run_query(Q2_DISSIMILAR, "Q2: 5 most dissimilar segments to '267:476'")
    else:
        print("\n⚠️  Q2: Not implemented yet")
    
    # Q3: Similar to neural network segment
    if Q3_NEURAL.strip():
        run_query(Q3_NEURAL, "Q3: 5 most similar segments to '48:511' (neural networks)")
    else:
        print("\n⚠️  Q3: Not implemented yet")
    
    # Q4: Similar to dark energy segment
    if Q4_PHYSICS.strip():
        run_query(Q4_PHYSICS, "Q4: 5 most similar segments to '51:56' (dark energy)")
    else:
        print("\n⚠️  Q4: Not implemented yet")
    
    # Q5: Most similar episodes
    if Q5A_EPISODE.strip():
        run_query(Q5A_EPISODE, "Q5a: 5 most similar episodes to segment '267:476'")
    else:
        print("\n⚠️  Q5a: Not implemented yet")
        
    if Q5B_EPISODE.strip():
        run_query(Q5B_EPISODE, "Q5b: 5 most similar episodes to segment '48:511'")
    else:
        print("\n⚠️  Q5b: Not implemented yet")
        
    if Q5C_EPISODE.strip():
        run_query(Q5C_EPISODE, "Q5c: 5 most similar episodes to segment '51:56'")
    else:
        print("\n⚠️  Q5c: Not implemented yet")
    
    # Q6: Similar episodes to Balaji podcast
    if Q6_BALAJI.strip():
        run_query(Q6_BALAJI, "Q6: 5 most similar episodes to 'VeH7qKZr0WI' (Balaji)")
    else:
        print("\n⚠️  Q6: Not implemented yet")
    
    print("\n" + "="*60)
    print("✅ Query execution complete!")


if __name__ == "__main__":
    main()
