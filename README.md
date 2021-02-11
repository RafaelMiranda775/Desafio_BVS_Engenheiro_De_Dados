![Boa Vista SCPC](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/BVS.png)
# Desafio BoaVista SCPC Engenheiro de Dados
Este documento tem por finalidade descrever o passo a passo do processo de ingestão de dados e uma visualização (relatório) na plataforma GCP, além de compartilhar as decisões de 
arquitetura, implementação e instruções sobre como executar o software.

## Modelagem Conceitual dos Dados


## Desenho de Arquitetura
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Desenhoarquitetura.PNG)

Este desenho de arquitetura contempla a ingestão de dados de uma fonte externa do GCP com finalidade de criar um Datalake no Storage e um Data Warehouse no Big Query para que o time de Business Intelligence consiga tomar as melhores decisões de negócios.

A arquitetura conta com uma camada de ETL no Cloud DataProc que contemplará o uso do Spark que é uma ferramenta Big Data que tem o objetivo de processar grandes conjuntos de dados de forma paralela e distribuída, além de ser 100 vezes mais rápido pois processa tudo na memória.

O fluxo de Orquestração da Pipeline será gerenciado pelo Cloud Function e Composer, o Cloud Function funcionará como uma Trigger que executará uma Dag no Composer assim que o arquivo CSV chegar no bucket do Cloud Storage com finalidade de reduzir o tempo de carregamento dos dados no Big Query, o Composer terá o trabalho de criar um cluster Dataproc, executar um processo em Spark e desligar a máquina do Dataproc assim que o processamento acabar, seguindo as boas práticas do Google que faz menção sobre criar máquinas no Dataproc de forma preemptiva, além de executar uma task que irá carregar os arquivos processados para o Big Query e chamará uma procedure que atualizará os dados para uma segunda camada TRUSTED com dados Particionados e Clusterizados para melhor desempenho e economia no momento da consulta de dados.

## Escopo do Projeto 
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Escopo_do_Projeto.PNG)

## Premissas
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Premissas.PNG)
