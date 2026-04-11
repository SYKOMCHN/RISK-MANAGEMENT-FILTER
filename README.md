# RISK-MANAGEMENT-FILTER

## to install -
$pip install streamlit

## to verify -
$streamlit hello

## to run -
streamlit run app.py


## Phase 1: Data Generation (Mock Database)

For this project, we use a synthetic HR dataset to simulate a Big Data environment. To keep the repository lightweight and adhere to best practices, we do not upload massive CSV files to version control. All team members and evaluators must generate the mock database locally before running the application.

### Objective
The `data_generator.py` script creates a dataset of 10,000+ employee records. This script deliberately skews the statistical distribution of the `Department` quasi-identifier. It generates a massive "Engineering" department and an intentionally tiny "Executive" or "SpecialOps" department. This intentional imbalance is required to successfully demonstrate and test the system's K-Anonymity threat assessment mechanisms.

### Setup & Execution

1. **Install Dependencies:** Ensure you have the required data science libraries installed.
   ```bash
   pip install -r requirements.txt