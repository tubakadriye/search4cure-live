from google.cloud import spanner
import os

from dotenv import load_dotenv

load_dotenv()

# Config
PROJECT_ID = os.getenv("PROJECT_ID", "search4cure-diabetes")
INSTANCE_ID = os.getenv("INSTANCE_ID", "diabetes-research-network")
DATABASE_ID = os.getenv("DATABASE_ID", "research-graph-db")

def get_database():
    # Create Spanner client
    client = spanner.Client(project=PROJECT_ID)
    
    # Provide proper instance
    instance = client.instance(INSTANCE_ID)
    
    # Get database
    database = instance.database(DATABASE_ID)

    return database
