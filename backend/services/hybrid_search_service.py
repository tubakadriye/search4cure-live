from backend.database.spanner_client import get_database

def run_spanner_query(sql, params=None):

    database = get_database()

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(sql, params=params or {})

        rows = []
        for row in results:
            rows.append(dict(row))

        return rows

# ---------------------------
# Semantic Paper Search
# ---------------------------

def semantic_paper_search(query, limit=10):

    sql = """
    WITH query_embedding AS (
        SELECT embeddings.values AS val
        FROM ML.PREDICT(
            MODEL TextEmbeddings,
            (SELECT @query AS content)
        )
    )

    SELECT
        p.paper_id,
        p.title,
        COSINE_DISTANCE(
            p.text_embedding,
            (SELECT val FROM query_embedding)
        ) AS distance

    FROM Papers p
    WHERE p.text_embedding IS NOT NULL
    ORDER BY distance
    LIMIT @limit
    """

    return run_spanner_query(sql, {"query": query, "limit": limit})

# ---------------------------
# Graph Search
# ---------------------------

def graph_method_search(disease):

    sql = """
    SELECT
        p.title,
        m.name AS method

    FROM Papers p
    JOIN PaperStudiesDisease psd
        ON p.paper_id = psd.paper_id

    JOIN PaperUsesMethod pum
        ON p.paper_id = pum.paper_id

    JOIN Methods m
        ON pum.method_id = m.method_id

    JOIN Diseases d
        ON psd.disease_id = d.disease_id

    WHERE LOWER(d.name) LIKE LOWER(@disease)
    """

    return run_spanner_query(sql, {"disease": f"%{disease}%"})

# ---------------------------
# Image Search
# ---------------------------

def image_search(query):

    sql = """
    WITH query_embedding AS (
        SELECT embeddings.values AS val
        FROM ML.PREDICT(
            MODEL TextEmbeddings,
            (SELECT @query AS content)
        )
    )

    SELECT
        image_id,
        gcs_key,
        caption,
        COSINE_DISTANCE(
            caption_embedding,
            (SELECT val FROM query_embedding)
        ) AS distance

    FROM Images
    ORDER BY distance
    LIMIT 5
    """

    return run_spanner_query(sql, {"query": query})

# ---------------------------
# Table Search
# ---------------------------

def table_search(query):

    sql = """
    WITH query_embedding AS (
        SELECT embeddings.values AS val
        FROM ML.PREDICT(
            MODEL TextEmbeddings,
            (SELECT @query AS content)
        )
    )

    SELECT
        table_id,
        paper_id,
        COSINE_DISTANCE(
            table_embedding,
            (SELECT val FROM query_embedding)
        ) AS distance

    FROM Tables
    ORDER BY distance
    LIMIT 5
    """

    return run_spanner_query(sql, {"query": query})




