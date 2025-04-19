#  PostgreSQL Setup with Docker for Vanna Copilot

This guide walks you through creating a PostgreSQL database using Docker, managing it via PGAdmin, and loading a `jobs_data.csv` file into a `jobs_data` table.

---

##  Step 1: Run PostgreSQL and PGAdmin Containers

Start PostgreSQL container:

```bash
docker run --name postgres \
  -e POSTGRES_PASSWORD=pg1234 \
  -p 5432:5432 \
  -d postgres
```

Start PGAdmin container:

```bash
docker run --name pgadmin-container \
  -p 5050:80 \
  -e PGADMIN_DEFAULT_EMAIL=sn964723@ohio.edu \
  -e PGADMIN_DEFAULT_PASSWORD=pga1234 \
  -d dpage/pgadmin4
```

Get the PostgreSQL container's IP address:

```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres
```

---

##  Step 2: Access PGAdmin

1. Open Docker Desktop and ensure both containers are running.
2. Open your browser and go to: `http://localhost:5050`
3. Log in using:
   - **Email:** `sn964723@ohio.edu`
   - **Password:** `pga1234`

---

##  Step 3: Register PostgreSQL Server in PGAdmin

1. Click **Servers > Register > Server**
2. In the **General** tab:
   - Name: `PostgreSQL Vanna DB`
3. In the **Connection** tab:
   - **Host name/address:** `172.17.0.2` (use output from earlier `docker inspect` command)
   - **Port:** `5432`
   - **Maintenance Database:** `postgres`
   - **Username:** `postgres`
   - **Password:** `pg1234`
   - Check ✔️ to save password
4. Click **Save**

---

##  Step 4: Create `jobs_data` Table

1. Navigate to: `Servers > Databases > postgres > Schemas > public > Tables`
2. Right-click on **Tables > Query Tool**
3. Paste the following SQL and run it:

```sql
CREATE TABLE jobs_data (
    work_year bigint,
    job_title character varying,
    job_category character varying,
    salary_currency character varying,
    salary bigint,
    salary_in_usd bigint,
    employee_residence character varying,
    experience_level character varying,
    employment_type character varying,
    work_setting character varying,
    company_location character varying,
    company_size character varying
);
```

 After running: *"Query returned successfully in 110 msec."*

---

##  Step 5: Import CSV into `jobs_data` Table

1. Right-click on the `jobs_data` table → Click **Import/Export Data**
2. In the **Import** tab:
   - **Filename:** Upload `jobs_data.csv`
   - Configure column mappings if necessary
3. Click **OK** to import the data

---

##  Step 6: Build Vanna Copilot with Ollama + ChromaDB

> This step integrates [Vanna.AI](https://vanna.ai/) with an **LLM backend (Ollama)** and a **vector database (ChromaDB)** for SQL generation and analysis.

---

###  Step 6.1: Import Vanna Modules

```python
from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore
```

---

###  Step 6.2: Create a Hybrid Vanna Class

```python
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)

vn = MyVanna(config={'model': 'llama3'})
```

---

###  Step 6.3: Connect Vanna to PostgreSQL

```python
vn.connect_to_postgres(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="pg1234"
)
```

---

###  Step 6.4: Load Schema Information

```python
information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
```

---

###  Step 6.5: Generate Training Plan

```python
plan = vn.get_training_plan_generic(information_schema)
vn.train(plan)
```

---

###  Step 6.6: Ask Questions in Natural Language

```python
vn.ask("What is the average salary for each job category?")
```

---

##  Requirements

Install Python packages:

```bash
pip install vanna ollama chromadb psycopg2
```

Start the LLM locally:

```bash
ollama run llama3
```

---

##  Vanna Copilot Overview

| Component     | Tool Used          |
|---------------|--------------------|
| LLM           | LLaMA 3 via Ollama |
| Vector Store  | ChromaDB           |
| SQL Generator | Vanna.AI           |
| Database      | PostgreSQL (Docker)|
| UI (optional) | Streamlit or CLI   |

---

##  Credentials Summary

| Component  | Value                  |
|------------|------------------------|
| PGAdmin URL | `http://localhost:5050` |
| PGAdmin Email | `sn964723@ohio.edu`  |
| PGAdmin Password | `pga1234`       |
| PostgreSQL Username | `postgres`  |
| PostgreSQL Password | `pg1234`    |"# -Vanna_Copilot" 
