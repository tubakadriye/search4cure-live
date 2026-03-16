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

        m.name AS method,
        d.name AS disease,

        COSINE_DISTANCE(
            p.text_embedding,
            (SELECT val FROM query_embedding)
        ) AS paper_distance,

        COSINE_DISTANCE(
            pg.text_embedding,
            (SELECT val FROM query_embedding)
        ) AS page_distance
    
    FROM Papers p

    LEFT JOIN Pages pg
        ON p.paper_id = pg.paper_id

    LEFT JOIN PaperUsesMethod pum
        ON p.paper_id = pum.paper_id

    LEFT JOIN Methods m
        ON pum.method_id = m.method_id

    LEFT JOIN PaperStudiesDisease psd
        ON p.paper_id = psd.paper_id

    LEFT JOIN Diseases d
        ON psd.disease_id = d.disease_id

    WHERE p.text_embedding IS NOT NULL

    ORDER BY distance ASC
    LIMIT @limit
    """

    return run_spanner_query(sql, {"query": query, "limit": limit})

def page_semantic_search(query, limit=10):

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
        pg.page_number,
        pg.text,

        COSINE_DISTANCE(
            pg.text_embedding,
            (SELECT val FROM query_embedding)
        ) AS distance

    FROM Pages pg
    JOIN Papers p
        ON pg.paper_id = p.paper_id

    WHERE pg.text_embedding IS NOT NULL

    ORDER BY distance ASC
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



# ---------------------------
# Keyword Search (BM25 style)
# ---------------------------

def keyword_paper_search(query, limit=20):

    sql = """
    SELECT
        paper_id,
        title,
        SCORE(title, @query) AS score
    FROM Papers
    WHERE SEARCH(title, @query)
    ORDER BY score DESC
    LIMIT @limit
    """

    return run_spanner_query(sql, {"query": query, "limit": limit})


# ---------------------------
# RRF Hybrid Search
# ---------------------------

def hybrid_rrf_search(query, limit=10, k=60):

    semantic_results = semantic_paper_search(query, limit=30)
    keyword_results = keyword_paper_search(query, limit=30)

    scores = {}
    paper_info = {}

    def add_scores(results):
        for rank, r in enumerate(results):
            pid = r["paper_id"]

            paper_info[pid] = r
            scores.setdefault(pid, 0)

            scores[pid] += 1 / (k + rank + 1)

    add_scores(semantic_results)
    add_scores(keyword_results)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    final = []

    for pid, score in ranked[:limit]:
        r = paper_info.get(pid)
        final.append({
            "paper_id": pid,
            "title": r.get("title"),
            "score": score
        })

    return final




