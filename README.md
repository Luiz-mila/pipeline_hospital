# 🏥 Pipeline Hospital

An end-to-end **Data Engineering pipeline** processing real hospital inpatient discharge records from New York State (2015), built as a portfolio project targeting a Data Engineering role in **Healthcare Sector**.

---

## 📋 Project Overview

This project implements a production-grade ETL pipeline that ingests, validates, cleans, transforms, and loads hospital discharge records into a PostgreSQL database, orchestrated by Apache Airflow running in Docker.

**Dataset:** [Hospital Inpatient Discharges (SPARCS De-Identified) — 2015](https://www.kaggle.com/datasets/thedevastator/2015-inpatient-discharges-sparcs-de-identified)  
**Source:** New York State Department of Health  
**Size:** ~883MB · 2.5M+ rows · 37 columns

---

## 🏗️ Architecture

hospital_records.csv
↓
Apache Airflow DAG
↓
┌──────────────────┐
│ validate_file │ — checks file exists and is not empty
└────────┬─────────┘
↓
┌──────────────────┐
│ read_csv │ — loads first 10,000 rows with Pandas
└────────┬─────────┘
↓
┌──────────────────┐
│ data_quality │ — null counts, dtype analysis, financial cols check
└────────┬─────────┘
↓
┌──────────────────┐
│ clean │ — fixes financial cols, fills nulls
└────────┬─────────┘
↓
┌──────────────────┐
│ transform │ — creates charge_cost_ratio, length_of_stay_numeric, is_emergency
└────────┬─────────┘
↓
┌──────────────────┐
│ load_to_postgres │ — loads 10,000 rows into PostgreSQL
└────────┬─────────┘
↓
PostgreSQL
↓
SQL Analytics

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| Apache Airflow 2.9.3 | Pipeline orchestration |
| Python 3.12 | ETL logic |
| Pandas | Data processing |
| PostgreSQL 16 | Data storage |
| SQLAlchemy | Database connection |
| Docker + Docker Compose | Reproducible environment |
| Git + GitHub | Version control and portfolio |

---

## 📁 Project Structure

pipeline_hospital/
│
├── data/ # Raw dataset (not versioned — too large)
│ └── hospital_records.csv
│
├── dags/
│ └── pipeline_hospital.py # Airflow DAG — full pipeline definition
│
├── src/
│ ├── etl/
│ │ ├── read_csv.py   # Reads CSV with Pandas
│ │ ├── data_quality.py   # Quality analysis — nulls, dtypes
│ │ ├── clean.py   # Cleans financial cols and nulls
│ │ ├── transform.py # Creates engineered features
│ │ └── load.py   # Loads to PostgreSQL via SQLAlchemy
│ │
│ └── utils/
│ └── file_validation.py   # Validates file existence and size
│
├── sql/
│ └── analysis.sql   # Analytical SQL queries
│
├── docker-compose.yaml   # Airflow + PostgreSQL environment
├── requirements.txt   # Python dependencies
├── .gitignore   # Excludes data, logs, credentials
└── README.md

---

## 🔍 Key SQL Insights

**Average cost by region (New York State):**

| Region | Avg Cost | Avg Charge/Cost Ratio |
|---|---|---|
| New York City | $11,798 | 2.66x |
| Hudson Valley | $10,059 | 3.17x |
| Western NY | $8,870 | 1.80x |
| Long Island | $8,206 | 4.13x |

**Top diagnoses by volume:**

| Diagnosis | Cases | Avg Cost |
|---|---|---|
| Mood disorders | 1,014 | $9,402 |
| Liveborn | 913 | $1,296 |
| Septicemia | 605 | $13,811 |
| Asthma | 579 | $7,777 |

---

## 🚀 How to Run

**Prerequisites:** Docker Desktop, WSL2 (Windows) or Linux/macOS

```bash
# 1. Clone the repository
git clone https://github.com/Luiz-mila/pipeline_hospital.git
cd pipeline_hospital

# 2. Add the dataset
# Download from Kaggle and rename to hospital_records.csv
# Place it inside the data/ folder

# 3. Set up environment
echo "AIRFLOW_UID=$(id -u)" > .env

# 4. Initialize Airflow
docker compose up airflow-init

# 5. Start all services
docker compose up -d

# 6. Access Airflow UI
# Open http://localhost:8080
# Login: admin / admin

# 7. Trigger the DAG
# Click on hospital_pipeline → Trigger DAG ▶
```

---

## 📊 Pipeline Results

- ✅ 10,000 hospital records processed end-to-end
- ✅ 3 engineered features created (`charge_cost_ratio`, `length_of_stay_numeric`, `is_emergency`)
- ✅ Financial columns cleaned and converted to numeric
- ✅ 12 columns with nulls treated
- ✅ Data loaded into PostgreSQL and validated via SQL queries
- ✅ Fully reproducible via Docker Compose

---

## 📌 Next Steps

- [ ] Scale to full dataset (2.5M+ rows) with chunked processing
- [ ] Add data quality tests with Great Expectations
- [ ] Build dashboard with Apache Superset or Power BI
- [ ] Deploy to AWS (S3 + RDS + MWAA)

---

## 🧠 About the Author

**Luiz Milaré**  
Data Engineer | SQL · Python · Airflow · PostgreSQL · Docker · Snowflake · Power BI  
📍 Paris, France  
📧 milahercu@gmail.com  
🔗 [GitHub](https://github.com/Luiz-mila) · [LinkedIn](https://www.linkedin.com/in/luiz-milaré)

Data Engineer and BI Analyst with hands-on experience building ETL pipelines, data warehouses, and analytical dashboards. Certified in Snowflake SQL and holder of a RNCP Level 6 Data Engineering certification. Fluent in Portuguese, French, English, and Italian — working across international data environments with a focus on healthcare, finance, and e-commerce domains.