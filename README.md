# Formstack Data Pipeline

This project sets up a data pipeline using [dlt](https://dlthub.com/) to pull form and submission data from Formstack's API, process it, and load it into a DuckDB database. The pipeline handles transforming and flattening the submission data so that each form field in the submission data is represented as a row in the DuckDB table.

## Getting Started

Follow these steps to set up and run the project:

### 1. Setup a Virtual Environment with Poetry

This project uses [Poetry](https://python-poetry.org/) to manage dependencies and create a virtual environment. If you don't have Poetry installed, you can install it by following the instructions [here](https://python-poetry.org/docs/#installation).

#### Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
#### Clone the Repository:
```bash
git clone <repository-url>
cd <repository-directory>
```
#### Install Dependencies:

Once inside the project directory, run the following command to install all dependencies:
```bash
poetry install
```
#### Activate the Virtual Environment:
```bash
poetry shell
```
### 2. Setup the `.dlt/secrets.toml` File

To authenticate with Formstack, you need to set up your API credentials in a `.dlt/secrets.toml` file. This file should be placed in the `.dlt/` directory of your project. 

#### Create `.dlt/secrets.toml`:
```bash
mkdir -p .dlt
touch .dlt/secrets.toml
```
#### Add your Formstack API secret key:

```
# .dlt/secrets.toml

api_secret_key = "your_formstack_api_secret_key_here"
```

Make sure to replace `"your_formstack_api_secret_key_here"` with your actual Formstack API secret key.

### 3. Run the Pipeline

To run the pipeline and pull data from the Formstack API, simply run the `formstack.py` script:
```python
python3 formstack.py
```
This will:
1. Load form metadata from the Formstack API.
2. Query form submission data for each form.
3. Flatten the form submission data and load it into a DuckDB database.

### DuckDB Database

By default, the data is loaded into a DuckDB file located at `scc_formstack.duckdb`. You can interact with the database using DuckDB’s command-line interface or other tools that support DuckDB.

### Additional Information

- **Schema Management**: The pipeline uses dlt's schema management functionality. The schema is automatically updated as new fields are encountered in the data.
- **Transformation**: The script transforms the nested JSON data from Formstack's API so that each field in the submission data is stored as its own row in the DuckDB table.

### Troubleshooting

- **API Issues**: Make sure that your API secret key in the `.dlt/secrets.toml` file is correct. Invalid or expired API keys will cause authentication errors.
- **Poetry Issues**: If you run into issues with Poetry, you can troubleshoot by visiting the [Poetry documentation](https://python-poetry.org/docs/).

---

### Dependencies

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- [dlt](https://dlthub.com/)
- [DuckDB](https://duckdb.org/)

