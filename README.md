![Boa Vista SCPC](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/BVS.png)
# Desafio BoaVista SCPC Engenheiro de Dados
Este documento tem por finalidade descrever o passo a passo do processo de ingestão de dados e uma visualização (relatório) na plataforma GCP, além de compartilhar as decisões de 
arquitetura, implementação e instruções sobre como executar o software.

## Modelagem Conceitual dos Dados


## Desenho de Arquitetura
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Desenhoarquitetura.PNG)

Este desenho de arquitetura contempla a ingestão de dados de uma fonte externa do GCP com finalidade de criar um Datalake no Storage e um Data Warehouse no Big Query para que o time de Business Intelligence consiga tomar as melhores decisões de negócios.

A arquitetura conta com uma camada de ETL no Cloud Dataproc que contemplará o uso do Spark que é uma ferramenta Big Data que tem o objetivo de processar grandes conjuntos de dados de forma paralela e distribuída, além de ser 100 vezes mais rápido pois processa tudo na memória.

O fluxo de orquestração da pipeline será gerenciado pelo Cloud Function e Composer, o Cloud Function funcionará como uma Trigger que executará uma Dag no Composer assim que o arquivo CSV chegar no bucket do Cloud Storage com finalidade de reduzir o tempo de carregamento dos dados no Big Query, o Composer terá o trabalho de criar um cluster Dataproc, executar um processo em Spark e desligar a máquina do Dataproc assim que o processamento acabar, seguindo as boas práticas do Google que faz menção sobre criar máquinas no Dataproc de forma preemptiva, além de executar uma task que irá carregar os arquivos processados para o Big Query e chamará uma procedure que atualizará os dados para uma segunda camada TRUSTED com dados Particionados e Clusterizados para melhor desempenho e economia no momento da consulta de dados.

Toda a parte de Segurança será feita pelos papéis padrões do IAM.

## Escopo do Projeto 
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Escopo_do_Projeto.PNG)

## Premissas
![Desenho Premissas](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Premissas.PNG)

## Infraestrutura
![Desenho Infraestrutura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/terraform.png) 

Toda nossa infraestrutura será escrita com Terraform que é uma ferramenta para construir, alterar e configurar infraestrutura de maneira segura e eficiente. A ferramenta tem incontáveis benefícios que possibilitam criar toda a infraestrutura em ambiente de desenvolvimento e com alguns cliques conseguimos replicar tudo que foi feito para ambientes diferentes como Homologação ou Produção por exemplo, além de ser MultiCloud.

## Cloud Storage 
![pastas_bucket](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/pastas_bucket.PNG) 

Organizei as pastas do Storage por arquivo e ferramenta.

![file_bill_of_materials](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_bill_of_materials.PNG) 

Cada pasta de arquivo receberá o arquivo original.

## Cloud Dataproc
![job_pyspark_example](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/job_pyspark.PNG)
![jobs_pyspark_finalizado](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/job_pyspark_finalizado.PNG)

A fase de ETL dos arquivos será execultada em forma de Job no Dataproc com Pyspark, essa execução tem como objetivo a transformação dos dados de CSV para Parquet pois o tipo de dado Parquet oferece muitos benefícios como reduzir o espaço de armazenamento no Cloud Storage, execução mais rápido em determinadas operações, schema automático das tabelas além de ser um dos formatos preferidos do Big Query.  

## Cloud Storage 

![Depois processamento Dataproc](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/processamento_dataproc_finalizado.PNG)
![file_backup](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_backup.png)
![file_processado](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_processado.PNG)

O job Spark do Cloud Dataproc executa uma rotina e cria duas pastas, uma com nome backup e a outra com nome processados, na pasta de backup está o arquivo original com a data de processamento, na pasta processados tem uma pasta com nome do arquivo e a data de processamento, dentro dessa pasta estão os arquivos parquet totalmente convertidos e com o tamanho bem menor em comparação com o arquivo CSV original.







