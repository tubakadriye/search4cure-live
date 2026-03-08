from google.cloud import spanner
import argparse, os, time
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
    """Insert sample data for nodes and edges."""
    def insert_nodes(txn):
        # Papers
        txn.insert(
            "Papers",
            columns=["paper_id", "title", "abstract", "publication_date", "journal"],
            values=[
                ("paper_001", "Predicting Diabetes Progression with Deep Learning", 
                 "We applied LSTM to predict HbA1c levels in type 2 diabetes.", 
                 "2023-05-15", "Diabetes Journal")
            ]
        )
        # Authors
        txn.insert("Authors", ["author_id","name","affiliation"], 
                   [("author_001","Alice Chen","University X")])
        # Methods
        txn.insert("Methods", ["method_id","name","category"],
                   [("method_lstm","LSTM","Deep Learning")])
        # Datasets
        txn.insert("Datasets", ["dataset_id","name","description"],
                   [("dataset_ukb","UK Biobank","Large scale biomedical dataset")])
        # Diseases
        txn.insert("Diseases", ["disease_id","name","type"],
                   [("disease_t2d","Type 2 Diabetes","Metabolic")])
        # Biomarkers
        txn.insert("Biomarkers", ["biomarker_id","name","unit"],
                   [("biomarker_hba1c","HbA1c","%")])
        # Drugs
        txn.insert("Drugs", ["drug_id","name","mechanism"],
                   [("drug_metformin","Metformin","Reduces hepatic glucose production")])
    
    def insert_edges(txn):
        txn.insert("PaperUsesMethod", ["paper_id","method_id"], [("paper_001","method_lstm")])
        txn.insert("PaperStudiesDisease", ["paper_id","disease_id"], [("paper_001","disease_t2d")])
        txn.insert("PaperUsesDataset", ["paper_id","dataset_id"], [("paper_001","dataset_ukb")])
        txn.insert("PaperMentionsBiomarker", ["paper_id","biomarker_id"], [("paper_001","biomarker_hba1c")])
        txn.insert("DrugTreatsDisease", ["drug_id","disease_id"], [("drug_metformin","disease_t2d")])
        txn.insert("AuthorWrotePaper", ["author_id","paper_id"], [("author_001","paper_001")])
    
    database.run_in_transaction(insert_nodes)
    database.run_in_transaction(insert_edges)
    print("Sample diabetes research data inserted ✅")

def create_graph(database, graph_name):
    """Create property graph for diabetes research."""
    ddl = f"""
    CREATE OR REPLACE PROPERTY GRAPH {graph_name}
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
        PaperUsesMethod KEY (paper_id, method_id) SOURCE KEY (paper_id) DESTINATION KEY (method_id) LABEL USES_METHOD,
        PaperStudiesDisease KEY (paper_id, disease_id) SOURCE KEY (paper_id) DESTINATION KEY (disease_id) LABEL STUDIES_DISEASE,
        PaperUsesDataset KEY (paper_id, dataset_id) SOURCE KEY (paper_id) DESTINATION KEY (dataset_id) LABEL USES_DATASET,
        PaperMentionsBiomarker KEY (paper_id, biomarker_id) SOURCE KEY (paper_id) DESTINATION KEY (biomarker_id) LABEL MENTIONS_BIOMARKER,
        DrugTreatsDisease KEY (drug_id, disease_id) SOURCE KEY (drug_id) DESTINATION KEY (disease_id) LABEL TREATS,
        AuthorWrotePaper KEY (author_id, paper_id) SOURCE KEY (author_id) DESTINATION KEY (paper_id) LABEL WROTE
      )
    """
    database.update_ddl([ddl]).result()
    print(f"Graph {graph_name} created ✅")
