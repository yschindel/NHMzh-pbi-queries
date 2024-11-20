import requests
import duckdb
import pandas as pd

def get_data_from_pbi_server(url, project, filename):
    params = {
        "name": filename,
        "project": project
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Server returned status {response.status_code}: {response.text}")
        
    return response.content

def get_all_data_files(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Server returned status {response.status_code}: {response.text}")
    return response.json()

# Example usage
url = "http://localhost:3000/data"
try:
    data_files = get_all_data_files(url + "/list")


    for file in data_files:
        project, filename = file.split("/")
        parquet_data = get_data_from_pbi_server(url, project, filename)

        print(f"Processing file: {filename}")
    
        # write to a temp file
        with open("temp_file.parquet", "wb") as f:
            f.write(parquet_data)
        
        # remove .parquet from filename
        filename = filename.replace(".parquet", "")

        try:
            # Insert with additional columns for project and filename
            duckdb.sql(f"""
                INSERT INTO data 
                SELECT 
                    '{project}' as project,
                    '{filename}' as filename,
                    *
                FROM temp_file.parquet
            """)
        except duckdb.CatalogException:
            # Create table with additional columns for project and filename
            duckdb.sql(f"""
                CREATE TABLE data AS 
                SELECT 
                    '{project}' as project,
                    '{filename}' as filename,
                    *
                FROM temp_file.parquet
            """)

        print(f"Number of rows in table: {duckdb.sql('SELECT COUNT(*) FROM data').fetchone()[0]}")

    # import the arrow table into pandas
    df = duckdb.sql("SELECT * FROM data").df()
    print(df)
except Exception as e:
    print(f"Error: {e}")