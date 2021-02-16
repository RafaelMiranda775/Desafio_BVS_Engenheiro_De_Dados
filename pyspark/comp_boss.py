# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
import os 
from datetime import datetime

# nome do bucket no storage
bucket = 'desafio-bvs'

# Data de Hoje 
data_e_hora_atuais = datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d-%m-%Y')

# Criando conexão com SparkSession
spark = SparkSession.builder.appName('desafioBVS').getOrCreate()

# Abrindo arquivo CSV
df = spark.read.csv("gs://"+bucket+"/comp_boss/*.csv", encoding="utf-8", sep=",", header=True)

# Printando Dataframe
df.show()

# Apagando arquivo do HDFS
os.system('hdfs dfs -rm -r comp_boss.parquet')

# Convertendo arquivo CSV para PARQUET
convert_parquet = df.write.parquet("comp_boss.parquet")

# Copiando arquivo parquet do HDFS para máquina local
os.system('hdfs dfs -copyToLocal comp_boss.parquet/ .')

# Copiando arquivo PARQUET de volta para o STORAGE com a DATA DE PROCESSAMENTO
os.system("gsutil -m mv comp_boss.parquet gs://{}/comp_boss/comp_boss_processado/comp_boss_{}.parquet"\
          .format(bucket, data_e_hora_em_texto))

# Copiando arquivo original para pasta de BACKUP com a DATA DE PROCESSAMENTO
os.system("gsutil -m mv gs://{}/comp_boss/comp_boss.csv gs://{}/comp_boss/comp_boss_backup/comp_boss_{}.csv"\
          .format(bucket, bucket, data_e_hora_em_texto))
