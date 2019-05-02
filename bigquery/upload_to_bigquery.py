# export GOOGLE_APPLICATION_CREDENTIALS="/Users/wan9838/Desktop/github/gcp/policygenius-d6114b1ed8b3.json"
# run above command to setup the api credentials
from google.cloud import bigquery
client = bigquery.Client()

def create_dataset(dataset_id):
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"

    dataset = client.create_dataset(dataset)
    print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

def create_table(table_id,schema):

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # API request
    print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))


def load_csv_from_local(filename):
    with open(filename, "rb") as source_file:
        print(source_file)
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # API request

    job.result()  # Waits for table load to complete.

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))

if __name__ == '__main__':

    project='policygenius'
    dataset_id = 'pg3'
    table_id ='t3'
    
    schema = [
    bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("last_name", "STRING", mode="REQUIRED"),
    ]
    
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    
    filename = 'data/1.csv'

    # to upload a csv, we dont need the table to be created beforehand.
    create_dataset(project+'.'+dataset_id)
    # create_table(project+'.'+dataset_id+'.'+table_id,schema)
    load_csv_from_local(filename)




