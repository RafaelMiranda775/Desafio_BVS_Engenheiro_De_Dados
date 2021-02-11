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
df = spark.read.csv("gs://desafio_bvs/price_quote/*.csv", encoding="utf-8", sep=",", header=True)

# Printando Dataframe
df.show()

# Apagando arquivo do HDFS
os.system('hdfs dfs -rm -r price_quote.parquet')

# Convertendo arquivo CSV para PARQUET
convert_parquet = df.write.parquet("price_quote.parquet")

# Copiando arquivo parquet do HDFS para máquina local
os.system('hdfs dfs -copyToLocal price_quote.parquet/ .')

# Copiando arquivo PARQUET de volta para o STORAGE com a DATA DE PROCESSAMENTO
os.system("gsutil -m mv price_quote.parquet gs://{}/price_quote/price_quote_processado/price_quote_{}.parquet"\
          .format(bucket, data_e_hora_em_texto))

# Copiando arquivo original para pasta de BACKUP com a DATA DE PROCESSAMENTO
os.system("gsutil -m mv gs://{}/price_quote/price_quote.csv gs://{}/price_quote/price_quote_backup/price_quote_{}.csv"\
          .format(bucket, bucket, data_e_hora_em_texto))
