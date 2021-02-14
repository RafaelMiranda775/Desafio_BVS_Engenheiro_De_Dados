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

## Cloud Storage 

![Depois processamento Dataproc](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/processamento_dataproc_finalizado.PNG)
![file_backup](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_backup.png)
![file_processado](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_processado.PNG)

O job Spark do Cloud Dataproc executa uma rotina e cria duas pastas, uma com nome backup e a outra com nome processados, na pasta de backup está o arquivo original com a data de processamento, na pasta processados tem uma pasta com nome do arquivo e a data de processamento, dentro dessa pasta estão os arquivos parquet totalmente convertidos e com o tamanho bem menor em comparação com o arquivo CSV original.

## Composer 

