from google.cloud import spanner
import os

PROJECT_ID = "search4cure-diabetes"
INSTANCE_ID = "diabetes-research-network"
DATABASE_ID = "research-graph-db"

from dotenv import load_dotenv

load_dotenv()

# Config
PROJECT_ID = os.getenv("PROJECT_ID")
INSTANCE_ID = os.getenv("INSTANCE_ID")
DATABASE_ID = os.getenv("DATABASE_ID")

def get_database():

    client = spanner.Client(project=PROJECT_ID)

    instance = client.instance(INSTANCE_ID)

    database = instance.database(DATABASE_ID)

    return database
