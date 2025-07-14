import os
from google.cloud import bigquery
import google.auth
import pandas as pd
from pyspark.sql import SparkSession
import findspark

# BigQuery Client
bq_client = bigquery.Client(project=os.environ['GOOGLE_CLOUD_PROJECT'], location=os.environ['LOCATION'])

# Spark Setup
findspark.init()
spark = SparkSession.builder \
    .master("local[*]") \
    .appName("BigQuery ML Spark") \
    .config("spark.jars", "path/to/spark-bigquery-connector.jar")  # Update path if needed \
    .getOrCreate()

def get_table_schema(client, dataset, table):
    try:
        table_ref = client.dataset(dataset).table(table)
        table = client.get_table(table_ref)
        schema_str = "Table Schema:\n"
        for schema_field in table.schema:
            schema_str += f"- {schema_field.name}: {schema_field.field_type}\n"
        return schema_str
    except Exception as e:
        return f"Error retrieving schema: {e}"

def execute_sql_query(query: str) -> pd.DataFrame:
    try:
        print("Executing BigQuery SQL query...")
        query_job = bq_client.query(query)
        results = query_job.to_dataframe()
        print("SQL query executed successfully.")
        return results
    except Exception as e:
        print(f"Error executing BigQuery query: {e}")
        return pd.DataFrame()

def execute_pyspark_code(code: str) -> pd.DataFrame:
    try:
        print("Executing PySpark ML code...")
        locals_dict = {'spark': spark, 'BQ_DATASET': os.environ['BQ_DATASET'], 'BQ_TABLE': os.environ['BQ_TABLE'], 'project_id': os.environ['GOOGLE_CLOUD_PROJECT']}
        exec(code, globals(), locals_dict)
        result_df = locals_dict.get('result_df')
        if result_df is None:
            raise ValueError("No 'result_df' defined in the code.")
        print("PySpark code executed successfully.")
        return result_df.toPandas()
    except Exception as e:
        print(f"Error executing PySpark code: {e}")
        return pd.DataFrame()
