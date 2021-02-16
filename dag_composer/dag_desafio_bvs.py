from airflow import DAG
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataprocClusterDeleteOperator,\
     DataProcPigOperator, DataProcPySparkOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
from airflow.contrib.operators import gcs_to_bq
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators import bigquery_operator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators import BashOperator, PythonOperator, bash_operator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStoragePrefixSensor 

# Dia de Hoje
now = datetime.now()
dia = now.strftime("%Y-%m-%d")
today = now.strftime("%d-%m-%Y")

# Variaveis do projeto
region = "us-east1"
zone = "us-east1-b"
project_id = "desafio-bvs-304714"
bucket = "desafio-bvs"

# Argumentos padrao do airflow
default_args = {
            "owner": "BVS",
            "depends_on_past": False,
            "start_date": datetime(2021,2,15), # Data de início da DAG
            "retries": 0,
        }


# Nome da dag, descricao, e frequencia de execucao
dag = DAG(
    dag_id="desafio_bvs",
    default_args = default_args,
    description = "Orquestração ingestão de dados",
    schedule_interval = "0 4 * * *" # Executar às 04:00 todo dia
    )

# Funcao que espera um determinado arquivo para começar a orquestracao
def storage_sensor(task, bucket_path, prefix_file):
    file_sensor = GoogleCloudStoragePrefixSensor(
            task_id='{}'.format(task, dia),  
            bucket=bucket,
            prefix='{}/{}'.format(bucket_path, prefix_file),
            dag=dag
        )

    return file_sensor 

# Executa script pyspark no Dataproc
def execute_script(task, script_storage, cluster):
    pyspark_operator = DataProcPySparkOperator(
            task_id='{}_{}'.format(task, dia),
            main=script_storage,
            cluster_name=cluster,
            region="us-central1",
            dag=dag
        )

    return pyspark_operator


# Cria cluster, qualquer alteracao de configuracao deve ser feita aqui
def create_cluster(task, cluster, status):
    cluster_dataproc = DataprocClusterCreateOperator(
        task_id = task,
        project_id = project_id,
        #service_account = 'composer-np-data-netezza@data-88d7.iam.gserviceaccount.com',
        cluster_name = cluster,
        num_workers = 2,
        region = "us-central1",
        zone = "us-central1-f",
        #num_preemptible_workers = 0,
        #metadata = dict(PIP_PACKAGES="google-cloud-storage pandas simpledbf"),  
        master_machine_type = "n1-standard-2",
        worker_machine_type = "n1-standard-2",
        master_disk_size = 15,
        worker_disk_size = 15,
        storage_bucket = bucket,
        #image_version = "1.3.82-debian10",
        trigger_rule=status,
        #subnetwork_uri = 'projects/np-network-ffe3/regions/southamerica-east1/subnetworks/data',
        #internal_ip_only = True,
        #auto_delete_ttl = 3600,
        dag = dag
    )

    return cluster_dataproc


# Deleta cluster, mas so se todos os jobs ja terminaram
def delete_cluster(task, cluster):
    del_cluster = DataprocClusterDeleteOperator(
            task_id = task,
            project_id = project_id,
            cluster_name = cluster,
            region = "us-central1",
            trigger_rule="all_done",
            dag=dag
        )

    return del_cluster

# Carrega arquivos no Big Query
def load_big_query(task, source_objects, table_name):
    load_big_query_operator = GoogleCloudStorageToBigQueryOperator(
        task_id=task,
        bucket=bucket,
        source_objects=[source_objects],
        source_format='PARQUET',
        create_disposition = 'CREATE_IF_NEEDED',
        destination_project_dataset_table= "{}:boa_vista.{}".format(project_id, table_name),
        write_disposition='WRITE_APPEND',
        time_partitioning={"type":"DAY"},
        encoding='utf-8',
        autodetect=True,
        ignore_unknown_values = True,
        #cluster_fields= True,
        dag=dag)

    return load_big_query_operator

# Chama as procedures
def procedures(task, procedure):
    sp_create_base_cluster = BigQueryOperator(
        task_id=task,
        bql=procedure,
        use_legacy_sql=False,
        dag=dag,
        depends_on_past=False)

    return sp_create_base_cluster

# Função que recebe um prefixo para inicio de orquestração
file_sensor_bill_of_materials = storage_sensor("file_sensor_bill_of_materials", "bill_of_materials", "bill_of_materials.csv")
file_sensor_comp_boss = storage_sensor("file_sensor_comp_boss", "comp_boss", "comp_boss.csv")
file_sensor_price_quote = storage_sensor("file_sensor_price_quote", "price_quote", "price_quote.csv")

# Função executa script .py
run_bill_of_materials = execute_script("spark_bill_of_materials","gs://"+bucket+"/pyspark/bill_of_materials.py", "cluster-bill-of-materials")
run_comp_boss = execute_script("spark_comp_boss","gs://"+bucket+"/pyspark/comp_boss.py", "cluster-comp-boss")
run_price_quote = execute_script("spark_price_quote","gs://"+bucket+"/pyspark/price_quote.py", "cluster-price-quote")

# Função cria cluster Dataproc dependendo do arquivo de prefixo que chegar no storage 
cluster_bill_of_materials = create_cluster("create_cluster_bill_of_materials", "cluster-bill-of-materials", "one_success")
cluster_comp_boss = create_cluster("create_cluster_comp_boss", "cluster-comp-boss", "one_success")
cluster_price_quote = create_cluster("create_cluster_price_quote", "cluster-price-quote", "one_success")

# Função deleta cluster
delete_cluster_bill_of_materials = delete_cluster("delete_cluster_bill_of_materials", "cluster-bill-of-materials")
delete_cluster_comp_boss = delete_cluster("delete_cluster_comp_boss", "cluster-comp-boss")
delete_cluster_price_quote = delete_cluster("delete_cluster_price_quote", "cluster-price-quote")

# Função carrega arquivos PARQUET no Big Query
load_bill_of_materials = load_big_query("load_table_bill_of_materials","bill_of_materials/bill_of_materials_processado/bill_of_materials_"+today+".parquet/*.parquet","bill_of_materials")
load_comp_boss = load_big_query("load_table_comp_boss","comp_boss/comp_boss_processado/comp_boss_"+today+".parquet/*.parquet","comp_boss")
load_price_quote = load_big_query("load_table_price_quote","price_quote/price_quote_processado/price_quote_"+today+".parquet/*.parquet","price_quote")

# Função chama as procedures do Big Query
sp_trusted_bill_of_materials = procedures("sp_trusted_bill_of_materials","CALL boa_vista_procedure.sp_trusted_bill_of_materials()")
sp_trusted_comp_boss = procedures("sp_trusted_comp_boss","CALL boa_vista_procedure.sp_trusted_comp_boss()")
sp_trusted_price_quote = procedures("sp_trusted_price_quote","CALL boa_vista_procedure.sp_trusted_price_quote()")

# Ordem de dependencias
file_sensor_bill_of_materials >> cluster_bill_of_materials >> run_bill_of_materials >> delete_cluster_bill_of_materials >> load_bill_of_materials >> sp_trusted_bill_of_materials

file_sensor_comp_boss >> cluster_comp_boss >> run_comp_boss >> delete_cluster_comp_boss >> load_comp_boss >> sp_trusted_comp_boss

file_sensor_price_quote >> cluster_price_quote >> run_price_quote >> delete_cluster_price_quote >> load_price_quote >> sp_trusted_price_quote
