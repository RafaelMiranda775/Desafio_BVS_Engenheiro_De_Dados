![Boa Vista SCPC](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/BVS.png)
# Desafio BoaVista SCPC Engenheiro de Dados
Este documento tem por finalidade descrever o passo a passo do processo de ingestão de dados e uma visualização (relatório) na plataforma GCP, além de compartilhar as decisões de 
arquitetura, implementação e instruções sobre como executar o software.

## Desenho de Arquitetura
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/arquitetura.PNG)

Este desenho de arquitetura contempla a ingestão de dados de uma fonte externa do GCP com finalidade de criar um Datalake no Storage e um Data Warehouse no Big Query para que o time de Business Intelligence consiga tomar as melhores decisões de negócios.

### Cloud Storage

A ferramenta Cloud Storage foi escolhida como Data Lake na nossa arquitetura pois fornece armazenamento dos arquivos ou como um backup de segurança para aqueles que já estão guardados em dispositivos físicos. Isso tudo com a segurança de que seus registros mais importantes não serão perdidos, danificados ou acessados por pessoas sem autorização. O mesmo também oferece Performance otimizada, Infraestrutura virtual ilimitada, ótimo custo-benefício, sincronização instantânea entre todos os aparelhos, alta escalabilidade entre outras.

### Cloud Dataproc
A arquitetura conta com uma camada de ETL no Cloud Dataproc que contemplará o uso do Spark que é uma ferramenta Big Data que tem o objetivo de processar grandes conjuntos de dados de forma paralela e distribuída, além de ser 100 vezes mais rápido pois processa tudo na memória.

### Big Query
O BigQuery foi contemplado na nossa arquitetura porque é um data warehouse totalmente gerenciado e sem servidor que permite análises escalonáveis em petabytes de dados. É uma plataforma como serviço (PaaS) que oferece suporte a consultas usando ANSI SQL. Ele também possui recursos integrados de aprendizado de máquina.

Quando emparelhado com o BI certo como Data Studio, pode ser uma ferramenta poderosa para qualquer negócio. Estas são algumas das principais razões pelas quais você deve considerar o Google BigQuery para suas ferramentas de BI.

### Composer 
O fluxo de orquestração da pipeline será gerenciado Composer, o mesmo terá o trabalho de criar um cluster Dataproc, executar um processo em Spark e desligar o cluster assim que o processamento acabar, seguindo as melhores práticas do Google que faz menção sobre criar cluster no Dataproc de forma preemptiva, além de executar uma task que irá carregar os arquivos processados para o Big Query e chamará uma procedure que atualizará os dados para uma segunda camada TRUSTED com dados Particionados e Clusterizados para melhor desempenho e economia no momento da consulta de dados.

### Cloud IAM
Toda a parte de Segurança será feita pelos papéis padrões do Google Cloud IAM ou Gerenciamento de identidades e acesso permitirá que os administradores decidam quem deve agir sobre os recursos e também abrange a auditoria interna.

### Data Studio 

Google Data Studio foi escolhido porque é uma ferramenta de dashboard do Google altamente personalizável e fácil de usar. É capaz de reunir diversas fontes de dados e extrair informações do Google Analytics, Google Ads, Search Console, YouTube e outras para criar relatórios e painéis informativos totalmente amigáveis.
Assim como os aplicativos no Google Drive, o Data Studio amplia a capacidade de colaboração nas equipes para otimizar a gestão de relatórios de equipes e também entre clientes externos.
Além do fato de ser gratuito – um motivo considerável – o Data Studio possui diversos recursos e vantagens para quem busca transformar dados em informações valiosas para os negócios.

## Escopo do Projeto 
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Escopo_do_Projeto.PNG)

## Premissas
![Desenho Premissas](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/premissas.PNG)

## Infraestrutura
![Desenho Infraestrutura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/terraform.png) 

Toda nossa infraestrutura será escrita com Terraform que é uma ferramenta para construir, alterar e configurar infraestrutura de maneira segura e eficiente. A ferramenta tem incontáveis benefícios que possibilitam criar toda a infraestrutura em ambiente de desenvolvimento e com alguns cliques conseguimos replicar tudo que foi feito para ambientes diferentes como Homologação ou Produção por exemplo, além de ser MultiCloud.

# Desenvolvimento 
## Terraform
Link de [instalação](https://learn.hashicorp.com/tutorials/terraform/install-cli) do <b>Terraform</b>  

Primeiramente iremos construir a infraestrutura do <b>Cloud Storage</b> que depende de uma <b>service account</b> com algumas permissões, coloquei na pasta <b>terraform</b> um <b> README.md</b> detalhando todas as permissões.

![terraform storage](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/project_id.PNG)

![terraform bucket name](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/bucket_name.PNG)

![terraform_folder_storage](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/folders.PNG)

Mude o <b>project id</b> e mude o <b>nome do bucket do Cloud Storage</b> pois o mesmo é <b>Global</b>.

 #### Execute os comandos abaixo:
```
1. terraform init -> para conectar a sua conta do GCP pela service account
```
![terraform init](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/terraform_init.PNG)

```
2. terraform plan -> para planejar o que será criado
```
![terraform plan](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/terraform_plan.PNG)

```
3. terraform apply -> para aprovar as mudanças
```
![terraform apply1](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/terraform_apply1.PNG)
![terraform apply2](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/terraform_apply2.PNG)

### Infraestrutura Composer e Big Query

O código de criação desses dois ambientes está na pasta <b>terraform</b>, a execução dos mesmos é bem parecida com o passo a passo feito acima, a única mudança é que no caso do Big Query e Composer os nomes não são <b>Globais</b> portanto não precisaram de mudanças.  

## Cloud Storage 
![pastas_bucket](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/cloud_storage.PNG) 

Organizei as pastas do Storage por arquivo e ferramenta.

![file_bill_of_materials](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_bill_of_materials.PNG) 

Cada pasta de arquivo receberá o arquivo original.

## Cloud Dataproc
![job_pyspark_example](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/job_pyspark.PNG)
![jobs_pyspark_finalizado](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/job_pyspark_finalizado.PNG)

A fase de ETL dos arquivos será execultada em forma de Job no Dataproc com Pyspark, essa execução tem como objetivo a transformação dos dados de CSV para Parquet pois o tipo de dado Parquet oferece muitos benefícios como reduzir o espaço de armazenamento no Cloud Storage, execução mais rápido em determinadas operações, schema automático das tabelas além de ser um dos formatos preferidos do Big Query.  

#### Exemplo SPARK
```
# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
import os 
from datetime import datetime

bucket = 'desafio_bvs'

# Data de Hoje 
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d-%m-%Y')

# Criando conexão com SparkSession
spark = SparkSession.builder.appName('desafioBVS').getOrCreate()

# Abrindo arquivo CSV
df = spark.read.csv("gs://desafio_bvs/bill_of_materials/*.csv", encoding="utf-8", sep=",", header=True)

# Printando Dataframe
df.show()

# Apagando arquivo do HDFS
os.system('hdfs dfs -rm -r bill_of_materials.parquet')

# Convertendo arquivo CSV para PARQUET
convert_parquet = df.write.parquet("bill_of_materials.parquet")

# Copiando arquivo parquet do HDFS para máquina local
os.system('hdfs dfs -copyToLocal bill_of_materials.parquet/ .')

# Copiando arquivo PARQUET de volta para o STORAGE com a DATA DE PROCESSAMENTO
os.system("gsutil -m mv bill_of_materials.parquet gs://{}/bill_of_materials/bill_of_materials_processado/bill_of_materials_{}.parquet"\
          .format(bucket, data_e_hora_em_texto))

# Copiando arquivo original para pasta de BACKUP com a DATA DE PROCESSAMENTO
os.system("gsutil -m mv gs://{}/bill_of_materials/bill_of_materials.csv gs://{}/bill_of_materials/bill_of_materials_backup/bill_of_materials_{}.csv"\
          .format(bucket, bucket, data_e_hora_em_texto))
```
Mude o nome da variável <b>bucket</b>.
## Cloud Storage 

![Depois processamento Dataproc](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/processamento_dataproc_finalizado.PNG)
![file_backup](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_backup.png)
![file_processado](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_processado.PNG)

O job Spark no Cloud Dataproc executa uma rotina e cria duas pastas, uma com nome backup e a outra com nome processados, na pasta de backup está o arquivo original com a data de processamento, na pasta processados tem uma pasta com nome do arquivo e a data de processamento, dentro dessa pasta estão os arquivos parquet totalmente convertidos e com o tamanho bem menor em comparação com o arquivo CSV original.

## Composer 
#### Ordem de Execução: 
![Tasks composer](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/Dag_composerFluxo.PNG)
![Ordem Execucao](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/ordem2.PNG)

O job Python no Composer executará a orquestração seguindo a ordem passada acima.

1. <b>file_sensor_bill_of_materials</b> -> Essa tarefa funcionará como um sensor que irá esperar um arquivo chegar na pasta <b>gs://desafio-bvs/bill_of_materials</b> com prefixo <b>bill_of_materials.csv</b>, quando o mesmo chegar essa Tarefa passará para <b>sucess</b> e a próxima tarefa do fluxo se iniciará. 

![Storage Sensor](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/storage_sensor.PNG)

#### Exemplo de <b>file_sensor_bill_of_materials</b> esperando arquivo com prefixo (bill_of_materials.csv) chegar: 
![sensor bill_of_materials](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/example_sensor.PNG)

2. <b>create_cluster_bill_of_materials </b> -> Essa tarefa do fluxo criará um cluster Dataproc com nome <b>cluster-bill-of-materials</b>.

![cria cluster dataproc](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/cria_cluster.PNG)

3. <b>spark_bill_of_materials_2021-02-15</b> -> Após a criação do cluster, executaremos o script <b>SPARK</b> que seguirá os passos descritos acima.

![pysparkoperator](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/pysparkoperator.PNG)

4. <b>delete_cluster_bill_of_materials </b> -> Quando o processo <b>SPARK</b> terminar o cluster será desligado seguindo o modo <b>preemptivo</b>.

![deleta cluster](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/deleta_cluster.PNG)

5. <b>load_table_bill_of_materials</b> -> Após o cluster ser desligado os dados serão carregados no dataset <b>boa_vista</b> com nome <b>bill_of_materials particionada por tempo de processamento</b>.

![load big query](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/big_query_operator.PNG)

![bigquery1](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/bigquery1.PNG)

Quando você cria uma tabela particionada por tempo de processamento, o BigQuery carrega automaticamente os dados em partições diárias baseadas em datas que refletem a hora de processamento ou chegada dos dados. Pseudocoluna e identificadores de sufixo permitem redefinir (substituir) e redirecionar dados para partições em um dia específico.

Nas tabelas particionadas por tempo de processamento, há uma pseudocoluna _PARTITIONTIME que contém um carimbo de data/hora baseado em data para os dados carregados nas tabelas. As consultas nas tabelas particionadas por tempo podem restringir os dados lidos fornecendo filtros _PARTITIONTIME que representam a localização de uma partição. Todos os dados na partição especificada são lidos pela consulta, mas o filtro de predicado _PARTITIONTIME restringe o número de partições verificadas.

![bigquery2](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/bigquery2.PNG)

6. <b>sp_trusted_bill_of_materials</b> -> Por último executaremos uma <b>Procedure</b> que fará o tratamento de alguns campos e criará uma camada <b>view</b> com os dados totalmente limpos e prontos para uso do time de business intelligence.

![procedures](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/procedures.PNG)

#### Procedure Big Query: 

![procedure1](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/procedure1.PNG)

#### Código PROCEDURE da tabela bill_of_materials
```
CREATE OR REPLACE PROCEDURE boa_vista_procedure.sp_trusted_bill_of_materials()
BEGIN
CREATE OR REPLACE VIEW boa_vista_view.bill_of_materials AS
SELECT
  tube_assembly_id,
   CASE
    WHEN component_id_1 = "NA" THEN NULL
  ELSE component_id_1 
  END AS component_id_1,
  CASE
    WHEN quantity_1 = "NA" THEN NULL 
  ELSE CAST(quantity_1 AS INT64) 
  END AS quantity_1,
   CASE
    WHEN component_id_2 = "NA" THEN NULL
  ELSE component_id_2 
  END AS component_id_2,
   CASE
    WHEN quantity_2 = "NA" THEN NULL
  ELSE CAST(quantity_2 AS INT64)
  END AS quantity_2, 
  CASE
    WHEN component_id_3 = "NA" THEN NULL
  ELSE component_id_3 
  END AS component_id_3,
   CASE
    WHEN quantity_3 = "NA" THEN NULL
  ELSE CAST(quantity_3 AS INT64) 
  END AS quantity_3,
   CASE
    WHEN component_id_4 = "NA" THEN NULL
  ELSE component_id_4 
  END AS component_id_4,
  CASE
    WHEN quantity_4 = "NA" THEN NULL
  ELSE CAST(quantity_4 AS INT64) 
  END AS quantity_4,
  CASE
    WHEN component_id_5 = "NA" THEN NULL
  ELSE component_id_5 
  END AS component_id_5,
  CASE
    WHEN quantity_5 = "NA" THEN NULL
  ELSE CAST(quantity_5 AS INT64) 
  END AS quantity_5,
    CASE
    WHEN component_id_6 = "NA" THEN NULL
  ELSE component_id_6 
  END AS component_id_6,
   CASE
    WHEN quantity_6 = "NA" THEN NULL
  ELSE CAST(quantity_6 AS INT64) 
  END AS quantity_6,
   CASE
    WHEN component_id_7 = "NA" THEN NULL
  ELSE component_id_7 
  END AS component_id_7,
   CASE
    WHEN quantity_7 = "NA" THEN NULL
  ELSE CAST(quantity_7 AS INT64) 
  END AS quantity_7,
  CASE
    WHEN component_id_8	 = "NA" THEN NULL
  ELSE component_id_8	 
  END AS component_id_8	,
  CASE
    WHEN quantity_8	 = "NA" THEN NULL
  ELSE CAST(quantity_8 AS INT64)	 
  END AS quantity_8	
  FROM `boa_vista.bill_of_materials`;
END;
```
#### Schema tabela bill_of_materials antes da execução da procedure
![schema antes da procedure](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/schema_bill_of_materials_antes_procedure.PNG)

#### Schema tabela bill_of_materials após execução de procedure 
![schema](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/bill_of_materials.PNG)

#### Amostra de dados da tabela 
![Amostra de dados](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/amostradedados_price_quote.PNG)

A orquestração será executada <b>todo dia as 04:00 da manhã</b>.

![Hora de Execução](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/hora_execu%C3%A7%C3%A3o.PNG)

#### Código DAG Composer
```
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
```
