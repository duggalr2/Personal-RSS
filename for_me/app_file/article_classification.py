from google.cloud import bigquery
from oauth2client.client import GoogleCredentials


GOOGLE_APPLICATION_CREDENTIALS = '/Users/Rahul/Desktop/side_projects/all_in_one/for_me'

client = bigquery.Client()

QUERY = (
    'SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` '
    'WHERE state = "TX" '
    'LIMIT 100')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)
