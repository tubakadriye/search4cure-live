from embeddings.text_embeddings import get_text_embedding
import pandas as pd

def embed_table(table_df: pd.DataFrame):
    """
    Convert a dataframe to text and embed it.
    """
    table_text = table_df.to_csv(index=False)
    embedding = get_text_embedding(table_text)
    return embedding
