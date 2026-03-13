-- =========================
-- PAPERS
-- =========================
CREATE TABLE Papers (
    paper_id STRING(36) NOT NULL,
    title STRING(MAX),
    abstract STRING(MAX),
    url STRING(MAX),
    text_embedding ARRAY<FLOAT32>(vector_length=>768),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)

) PRIMARY KEY (paper_id);

-- =========================
-- AUTHORS
-- =========================
CREATE TABLE Authors (
    author_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (author_id);

-- =========================
-- PAGES
-- =========================
CREATE TABLE Pages (
    page_id STRING(36) NOT NULL,
    paper_id STRING(36),
    page_number INT64,
    text STRING(MAX),
    text_embedding ARRAY<FLOAT32>(vector_length=>768),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (page_id);

-- =========================
-- IMAGES
-- =========================
CREATE TABLE Images (
    image_id STRING(36) NOT NULL,
    paper_id STRING(36),
    page_number INT64,
    gcs_key STRING(MAX),
    width INT64,
    height INT64,
    caption STRING(MAX),
    image_embedding ARRAY<FLOAT32>(vector_length=>1408),
    caption_embedding ARRAY<FLOAT32>(vector_length=>768),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (image_id);

-- =========================
-- TABLES
-- =========================
CREATE TABLE Tables (
    table_id STRING(36) NOT NULL,
    paper_id STRING(36),
    page_number INT64,
    table_json STRING(MAX),
    table_embedding ARRAY<FLOAT32>(vector_length=>768),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (table_id);

-- =========================
-- ENTITIES
-- =========================
CREATE TABLE Diseases (
    disease_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (disease_id);

CREATE TABLE Methods (
    method_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (method_id);

CREATE TABLE Datasets (
    dataset_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (dataset_id);

CREATE TABLE Biomarkers (
    biomarker_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (biomarker_id);

CREATE TABLE Drugs (
    drug_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (drug_id);

CREATE TABLE Genes (
    gene_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (gene_id);

CREATE TABLE Outcomes (
    outcome_id STRING(36) NOT NULL,
    name STRING(MAX),
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (outcome_id);

-- =========================
-- EDGES
-- =========================

CREATE TABLE PaperHasPage (
    paper_id STRING(36) NOT NULL,
    page_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, page_id),
INTERLEAVE IN PARENT Papers ON DELETE CASCADE;

CREATE TABLE PaperHasImage (
    paper_id STRING(36) NOT NULL,
    image_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, image_id);

CREATE TABLE PageHasImage (
    page_id STRING(36) NOT NULL,
    image_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (page_id, image_id);

CREATE TABLE PaperHasTable (
    paper_id STRING(36) NOT NULL,
    table_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, table_id);

CREATE TABLE PaperHasAuthor (
    paper_id STRING(36) NOT NULL,
    author_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, author_id);

CREATE TABLE PaperUsesMethod (
    paper_id STRING(36) NOT NULL,
    method_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, method_id);

CREATE TABLE PaperUsesDataset (
    paper_id STRING(36) NOT NULL,
    dataset_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, dataset_id);

CREATE TABLE PaperStudiesDisease (
    paper_id STRING(36) NOT NULL,
    disease_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, disease_id);

CREATE TABLE PaperMentionsBiomarker (
    paper_id STRING(36) NOT NULL,
    biomarker_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, biomarker_id);

CREATE TABLE PaperMentionsDrug (
    paper_id STRING(36) NOT NULL,
    drug_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, drug_id);

CREATE TABLE PaperMentionsGene (
    paper_id STRING(36) NOT NULL,
    gene_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, gene_id);

CREATE TABLE PaperMentionsOutcome (
    paper_id STRING(36) NOT NULL,
    outcome_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, outcome_id);

CREATE TABLE DrugTreatsDisease (
    drug_id STRING(36) NOT NULL,
    disease_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (drug_id, disease_id);

CREATE TABLE PaperCitesPaper (
    citing_paper_id STRING(36) NOT NULL,
    cited_paper_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY(citing_paper_id, cited_paper_id);

CREATE TABLE PaperReportsOutcome (
    paper_id STRING(36) NOT NULL,
    outcome_id STRING(36) NOT NULL,
    created_at TIMESTAMP OPTIONS (allow_commit_timestamp=true)
) PRIMARY KEY (paper_id, outcome_id);

-- =========================
-- VECTOR INDEXES
-- =========================

CREATE VECTOR INDEX idx_paper_embedding
ON Papers(text_embedding)
WHERE text_embedding IS NOT NULL
OPTIONS(distance_type="COSINE");

CREATE VECTOR INDEX idx_page_embedding
ON Pages(text_embedding)
WHERE text_embedding IS NOT NULL
OPTIONS(distance_type="COSINE");

CREATE VECTOR INDEX idx_image_embedding
ON Images(image_embedding)
WHERE image_embedding IS NOT NULL
OPTIONS(distance_type="COSINE");

CREATE VECTOR INDEX idx_caption_embedding
ON Images(caption_embedding)
WHERE caption_embedding IS NOT NULL
OPTIONS(distance_type="COSINE");

CREATE VECTOR INDEX idx_table_embedding
ON Tables(table_embedding)
WHERE table_embedding IS NOT NULL
OPTIONS(distance_type="COSINE");