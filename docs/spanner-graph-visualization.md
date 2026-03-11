# 🚀 Visualizing Diabetes Research Graph in Spanner Studio

This guide helps you explore the **Diabetes Research Network graph** stored in **Google Cloud Spanner**.

Open **Spanner Studio** and run Graph queries using:

```sql
GRAPH DiabetesGraph
MATCH result = (p:Paper)-[:STUDIES_DISEASE]->(d:Disease)
RETURN TO_JSON(result) AS json_result
```

Example result:

paper_001 → Type 2 Diabetes

## 1️⃣ Understanding the Graph Structure

Think of the dataset as a **research knowledge network**.

| Entity     | Role                | Analogy      |
| ---------- | ------------------- | ------------ |
| Papers     | Research studies    | Missions     |
| Authors    | Scientists          | Agents       |
| Methods    | Algorithms / models | Tools        |
| Datasets   | Research datasets   | Data sources |
| Diseases   | Medical conditions  | Targets      |
| Biomarkers | Clinical indicators | Signals      |
| Drugs      | Treatments          | Solutions    |


**Goal**

Connect:
```matlab

research papers → methods → datasets → diseases → biomarkers → drugs
```


This allows an **AI agent** to answer questions like:

- "Which papers used LSTM for diabetes prediction?"

- "Which drugs treat Type 2 Diabetes?"

- "Which biomarker is used to measure diabetes?"


## 2️⃣ Query 1 — Paper Research Map

See which papers study which diseases.

```sql
GRAPH DiabetesGraph
MATCH result = (p:Paper)-[:STUDIES_DISEASE]->(d:Disease)
RETURN TO_JSON(result) AS json_result
```

**Why this matters**

For researchers:

- Quickly find papers studying Type 2 Diabetes

- Understand research coverage

Example result:

```
paper_001 → Type 2 Diabetes
```


## 3️⃣ Query 2 — Methods Used in Research

Find what machine learning methods papers use.

```
GRAPH DiabetesGraph
MATCH result = (p:Paper)-[:USES_METHOD]->(m:Method)
RETURN TO_JSON(result) AS json_result
```


Example insight:

```
paper_001 → LSTM
```

**Why this matters**

The AI agent can answer questions like:

    "Which papers used deep learning?"

## 4️⃣ Query 3 — Dataset Usage

Find which datasets are used in research.

```sql
GRAPH DiabetesGraph
MATCH result = (p:Paper)-[:USES_DATASET]->(d:Dataset)
RETURN TO_JSON(result) AS json_result
```

Example result:

    paper_001 → UK Biobank

## 5️⃣ Query 4 — Biomarkers Mentioned

See which biomarkers papers analyze.

```sql
GRAPH DiabetesGraph
MATCH result = (p:Paper)-[:MENTIONS_BIOMARK]->(b:Biomarker)
RETURN TO_JSON(result) AS json_result
```

Example result:

    paper_001 → HbA1c

**Why this matters**

Biomarkers help measure disease progression.

## 6️⃣ Query 5 — Drug Treatments

Find drugs that treat diseases.

```sql
GRAPH DiabetesGraph
MATCH result = (drug:Drug)-[:TREATS]->(d:Disease)
RETURN TO_JSON(result) AS json_result
```

Example result:

    Metformin → Type 2 Diabetes

## 7️⃣ Query 6 — Author Contributions

Find which authors wrote which papers.

```sql
GRAPH DiabetesGraph
MATCH result = (a:Author)-[:WROTE]->(p:Paper)
RETURN TO_JSON(result) AS json_result
```

Example:

    Alice Chen → paper_001

## 8️⃣ Query 7 — Citation Network

Explore paper citation relationships.

```sql
GRAPH DiabetesGraph
MATCH result = (p1:Paper)-[:CITES_PAPER]->(p2:Paper)
RETURN TO_JSON(result) AS json_result
```

This reveals the knowledge flow between studies.

## Advanced Query — AI Research Discovery

This query finds papers studying diabetes that use ML methods and datasets.

```sql
GRAPH DiabetesGraph
MATCH result =
    (p:Paper)-[:STUDIES_DISEASE]->(d:Disease),
    (p)-[:USES_METHOD]->(m:Method),
    (p)-[:USES_DATASET]->(ds:Dataset)
RETURN TO_JSON(result) AS json_result
```

Example output:

```makefile
Paper: Predicting Diabetes Progression
Method: LSTM
Dataset: UK Biobank
Disease: Type 2 Diabetes
```

## How Your AI Agent Will Use This

Your Graph RAG agent will run queries like these when a user asks:

| User Question                         | Graph Query                |
| ------------------------------------- | -------------------------- |
| "Which papers study Type 2 Diabetes?" | Paper → Disease            |
| "Which method predicts HbA1c?"        | Paper → Biomarker → Method |
| "Which drug treats diabetes?"         | Drug → Disease             |



This allows **multi-hop reasoning across the research network**.

## Graph Visualization

When you run the queries in Spanner Studio, you will see a structure like:

```mathematica
Paper
  ├── USES_METHOD → Method
  ├── USES_DATASET → Dataset
  ├── STUDIES_DISEASE → Disease
  └── MENTIONS_BIOMARK → Biomarker

Author ── WROTE → Paper
Drug ── TREATS → Disease
Paper ── CITES_PAPER → Paper
```

