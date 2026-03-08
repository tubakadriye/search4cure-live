"""
Diabetes Research Network Database Setup Script
Run: python setup_database.py
Or:  python setup_database.py --project=your-project-id
"""

from google.cloud import spanner
from google.cloud.spanner_admin_instance_v1 import (
    Instance as InstancePB,
    CreateInstanceRequest,
)
from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
import argparse
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Config
INSTANCE_ID = os.getenv("INSTANCE_ID", "research-network")
DATABASE_ID = os.getenv("DATABASE_ID", "graph-db")
GRAPH_NAME = os.getenv("GRAPH_NAME", "DiabetesGraph")
PROJECT_ID = os.getenv("PROJECT_ID", None)
REGION = os.getenv("REGION", "us-central1")

# DDL: Nodes and Edges
DDL_STATEMENTS = [
    # Nodes
    """CREATE TABLE Papers (
        paper_id STRING(36) NOT NULL,
        title STRING(MAX) NOT NULL,
        abstract STRING(MAX),
        publication_date DATE,
        journal STRING(100)
    ) PRIMARY KEY (paper_id)""",

    """CREATE TABLE Authors (
        author_id STRING(36) NOT NULL,
        name STRING(100) NOT NULL,
        affiliation STRING(200)
    ) PRIMARY KEY (author_id)""",

    """CREATE TABLE Methods (
        method_id STRING(36) NOT NULL,
        name STRING(100) NOT NULL,
        category STRING(50)
    ) PRIMARY KEY (method_id)""",

    """CREATE TABLE Datasets (
        dataset_id STRING(36) NOT NULL,
        name STRING(100) NOT NULL,
        description STRING(MAX)
    ) PRIMARY KEY (dataset_id)""",

    """CREATE TABLE Diseases (
        disease_id STRING(36) NOT NULL,
        name STRING(100) NOT NULL,
        type STRING(50)
    ) PRIMARY KEY (disease_id)""",

    """CREATE TABLE Biomarkers (
        biomarker_id STRING(36) NOT NULL,
        name STRING(100) NOT NULL,
        unit STRING(20)
    ) PRIMARY KEY (biomarker_id)""",

    """CREATE TABLE Drugs (
        drug_id STRING(36) NOT NULL,
        name STRING(100) NOT NULL,
        mechanism STRING(MAX)
    ) PRIMARY KEY (drug_id)""",

    # Edges
    """CREATE TABLE PaperUsesMethod (
        paper_id STRING(36) NOT NULL,
        method_id STRING(36) NOT NULL
    ) PRIMARY KEY (paper_id, method_id)""",

    """CREATE TABLE PaperStudiesDisease (
        paper_id STRING(36) NOT NULL,
        disease_id STRING(36) NOT NULL
    ) PRIMARY KEY (paper_id, disease_id)""",

    """CREATE TABLE PaperUsesDataset (
        paper_id STRING(36) NOT NULL,
        dataset_id STRING(36) NOT NULL
    ) PRIMARY KEY (paper_id, dataset_id)""",

    """CREATE TABLE PaperMentionsBiomarker (
        paper_id STRING(36) NOT NULL,
        biomarker_id STRING(36) NOT NULL
    ) PRIMARY KEY (paper_id, biomarker_id)""",

    """CREATE TABLE DrugTreatsDisease (
        drug_id STRING(36) NOT NULL,
        disease_id STRING(36) NOT NULL
    ) PRIMARY KEY (drug_id, disease_id)""",

    """CREATE TABLE AuthorWrotePaper (
        author_id STRING(36) NOT NULL,
        paper_id STRING(36) NOT NULL
    ) PRIMARY KEY (author_id, paper_id)""",
]

def insert_initial_data(database):
    """Insert sample node and edge data."""
    def insert_nodes(txn):
        txn.insert(
            "Papers",
            columns = ["paper_id", "title", "abstract", "publication_date", "journal"],
            values = [("paper_001", "Predicting Diabetes Progression with Deep Learning",
              "We applied LSTM to predict HbA1c levels in type 2 diabetes.",
              "2023-05-15", "Diabetes Journal")]
        )
        txn.insert("Authors", ["author_id","name","affiliation"], [("author_001","Alice Chen","University X")])
        txn.insert("Methods", ["method_id","name","category"], [("method_lstm","LSTM","Deep Learning")])
        txn.insert("Datasets", ["dataset_id","name","description"], [("dataset_ukb","UK Biobank","Large scale biomedical dataset")])
        txn.insert("Diseases", ["disease_id","name","type"], [("disease_t2d","Type 2 Diabetes","Metabolic")])
        txn.insert("Biomarkers", ["biomarker_id","name","unit"], [("biomarker_hba1c","HbA1c","%")])
        txn.insert("Drugs", ["drug_id","name","mechanism"], [("drug_metformin","Metformin","Reduces hepatic glucose production")])

    def insert_edges(txn):
        txn.insert("PaperUsesMethod", ["paper_id","method_id"], [("paper_001","method_lstm")])
        txn.insert("PaperStudiesDisease", ["paper_id","disease_id"], [("paper_001","disease_t2d")])
        txn.insert("PaperUsesDataset", ["paper_id","dataset_id"], [("paper_001","dataset_ukb")])
        txn.insert("PaperMentionsBiomarker", ["paper_id","biomarker_id"], [("paper_001","biomarker_hba1c")])
        txn.insert("DrugTreatsDisease", ["drug_id","disease_id"], [("drug_metformin","disease_t2d")])
        txn.insert("AuthorWrotePaper", ["author_id","paper_id"], [("author_001","paper_001")])

    print("Inserting node data...")
    database.run_in_transaction(insert_nodes)
    print("Inserting edge data...")
    database.run_in_transaction(insert_edges)
    print("Sample diabetes research data inserted ✅")

def create_graph(database, graph_name):
    ddl = f"""
    CREATE PROPERTY GRAPH {graph_name}
      NODE TABLES (
        Papers KEY (paper_id) LABEL Paper PROPERTIES (paper_id, title, abstract, publication_date, journal),
        Authors KEY (author_id) LABEL Author PROPERTIES (author_id, name, affiliation),
        Methods KEY (method_id) LABEL Method PROPERTIES (method_id, name, category),
        Datasets KEY (dataset_id) LABEL Dataset PROPERTIES (dataset_id, name, description),
        Diseases KEY (disease_id) LABEL Disease PROPERTIES (disease_id, name, type),
        Biomarkers KEY (biomarker_id) LABEL Biomarker PROPERTIES (biomarker_id, name, unit),
        Drugs KEY (drug_id) LABEL Drug PROPERTIES (drug_id, name, mechanism)
      )
      EDGE TABLES (
        PaperUsesMethod KEY (paper_id, method_id)
            SOURCE KEY (paper_id) REFERENCES Papers
            DESTINATION KEY (method_id) REFERENCES Methods
            LABEL USES_METHOD,
        PaperStudiesDisease KEY (paper_id, disease_id)
            SOURCE KEY (paper_id) REFERENCES Papers
            DESTINATION KEY (disease_id) REFERENCES Diseases
            LABEL STUDIES_DISEASE,
        PaperCitesPaper KEY (citing_paper_id, cited_paper_id)
            SOURCE KEY (citing_paper_id) REFERENCES Papers
            DESTINATION KEY (cited_paper_id) REFERENCES Papers
            LABEL CITES_PAPER,
        PaperHasAuthor KEY (paper_id, author_id)
            SOURCE KEY (paper_id) REFERENCES Papers
            DESTINATION KEY (author_id) REFERENCES Authors
            LABEL HAS_AUTHOR,
        PaperUsesDataset KEY (paper_id, dataset_id)
            SOURCE KEY (paper_id) REFERENCES Papers
            DESTINATION KEY (dataset_id) REFERENCES Datasets
            LABEL USES_DATASET,
        PaperMentionsBiomarker KEY (paper_id, biomarker_id)
            SOURCE KEY (paper_id) REFERENCES Papers
            DESTINATION KEY (biomarker_id) REFERENCES Biomarkers
            LABEL MENTIONS_BIOMARK,
        DrugTreatsDisease KEY (drug_id, disease_id)
            SOURCE KEY (drug_id) REFERENCES Drugs
            DESTINATION KEY (disease_id) REFERENCES Diseases
            LABEL TREATS,
        AuthorWrotePaper KEY (author_id, paper_id)
            SOURCE KEY (author_id) REFERENCES Authors
            DESTINATION KEY (paper_id) REFERENCES Papers
            LABEL WROTE
      )
    """
    print(f"Creating {graph_name}...")
    operation = database.update_ddl([ddl])
    operation.result()
    print(f"Graph {graph_name} created ✅")



def create_instance_with_enterprise(client, project_id, instance_id, region):
    """Create a Spanner instance with ENTERPRISE edition using the admin API."""
    config_name = f"projects/{project_id}/instanceConfigs/regional-{region}"
    instance_name = f"projects/{project_id}/instances/{instance_id}"
    
    instance_admin_client = client.instance_admin_api
    
    instance_pb = InstancePB(
        name=instance_name,
        config=config_name,
        display_name="Survivor Network",
        processing_units=100,
        edition=InstancePB.Edition.ENTERPRISE,
    )
    
    request = CreateInstanceRequest(
        parent=f"projects/{project_id}",
        instance_id=instance_id,
        instance=instance_pb,
    )
    
    operation = instance_admin_client.create_instance(request=request)
    return operation

def print_config(project_id, instance_id, database_id, graph_name, region):
    print("\n" + "="*60)
    print("Current Configuration (from environment or args):")
    print("="*60)
    print(f"  PROJECT_ID:   {project_id or 'Not set'}")
    print(f"  INSTANCE_ID:  {instance_id}")
    print(f"  DATABASE_ID:  {database_id}")
    print(f"  GRAPH_NAME:   {graph_name}")
    print(f"  REGION:       {region}")
    print("="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Setup Diabetes Research Database")
    parser.add_argument("--project", help="GCP Project ID (overrides env)")
    parser.add_argument("--instance", help="Spanner Instance ID (overrides env)")
    parser.add_argument("--database", help="Spanner Database ID (overrides env)")
    parser.add_argument("--graph", help="Graph name (overrides env)")
    parser.add_argument("--region", help="GCP Region (overrides env)")
    parser.add_argument("--skip-instance", action="store_true", help="Skip instance creation")
    parser.add_argument("--force", action="store_true", help="Delete & recreate database")
    parser.add_argument("--show-config", action="store_true", help="Show config and exit")
    args = parser.parse_args()

    project_id = args.project or PROJECT_ID
    instance_id = args.instance or INSTANCE_ID
    database_id = args.database or DATABASE_ID
    graph_name = args.graph or GRAPH_NAME
    region = args.region or REGION

    if args.show_config:
        print_config(project_id, instance_id, database_id, graph_name, region)
        return

    if not project_id:
        print("ERROR: PROJECT_ID is required.")
        return
    
    print("\n" + "=" * 60)
    print("Diabetes Research Database Setup")
    print("=" * 60)
    print(f"  Project:   {project_id}")
    print(f"  Instance:  {instance_id}")
    print(f"  Database:  {database_id}")
    print(f"  Graph:     {graph_name}")
    print(f"  Region:    {region}")
    print("=" * 60 + "\n")


    client = spanner.Client(project=project_id)

    instance = client.instance(instance_id)
    print("Checking instance exists...")
    instance_exists = instance.exists()
    print(f"Instance exists? {instance_exists}")

    if instance_exists:
        print(f"Instance {instance_id} already exists. Using existing instance.")
    elif not args.skip_instance:
        print(f"Creating instance {instance_id} with ENTERPRISE edition...")
        operation = create_instance_with_enterprise(client, project_id, instance_id, region)
        print("Waiting for instance creation (this may take a few minutes)...")
        operation.result()
        print("Instance created!")
        # Refresh instance reference
        instance = client.instance(instance_id)
    else:
        print("ERROR: Instance does not exist and --skip-instance was specified.")
        return

    database = instance.database(database_id)
    print("Checking database exists...")
    database_exists = database.exists()
    if database_exists:
        if args.force:
            print(f"Deleting existing database {database_id} (--force)...")
            operation = database.drop()
            print("Database deleted. Waiting 5 seconds...")
            time.sleep(5)
        else:
            print(f"Database {database_id} already exists. Use --force to recreate.")
            return

    print(f"Creating database {database_id}...")
    database = instance.database(database_id, ddl_statements=DDL_STATEMENTS)
    operation = database.create()
    print("Waiting for database to be ready...")
    operation.result()
    print("Database created!")

    # Insert data
    print("Inserting node data...")
    database = instance.database(database_id)
    insert_initial_data(database)
    print("Node data inserted ✅")

    print(f"Creating property graph {graph_name}...")
    create_graph(database, graph_name)

    print("\n" + "=" * 60)
    print("SUCCESS! Database setup complete.")
    print("=" * 60)
    print(f"\nInstance:  {instance_id}")
    print(f"Database:  {database_id}")
    print(f"Graph:     {graph_name}")
    print(f"\nAccess your database at:")
    print(f"https://console.cloud.google.com/spanner/instances/{instance_id}/databases/{database_id}?project={project_id}")


if __name__ == "__main__":
    main()
    os._exit(0)
