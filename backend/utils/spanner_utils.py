def paper_exists(database, paper_id):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT 1 FROM Papers WHERE paper_id = @paper_id LIMIT 1",
            params={"paper_id": paper_id},
            param_types={"paper_id": "STRING"},
        )
        return any(results)
    

def get_existing_papers(database):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql("SELECT paper_id FROM Papers")
        return set(row[0] for row in results)