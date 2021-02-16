# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
import os 
from datetime import datetime

bucket = 'desafio-bvs'

# Data de Hoje 
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d-%m-%Y')

# Criando conexão com SparkSession
spark = SparkSession.builder.appName('desafioBVS').getOrCreate()

# Abrindo arquivo CSV
df = spark.read.csv("gs://"+bucket+"/bill_of_materials/*.csv", encoding="utf-8", sep=",", header=True)

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
