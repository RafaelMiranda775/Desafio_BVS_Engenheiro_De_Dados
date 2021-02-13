![Boa Vista SCPC](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/BVS.png)
# Desafio BoaVista SCPC Engenheiro de Dados
Este documento tem por finalidade descrever o passo a passo do processo de ingestão de dados e uma visualização (relatório) na plataforma GCP, além de compartilhar as decisões de 
arquitetura, implementação e instruções sobre como executar o software.

## Modelagem Conceitual dos Dados


## Desenho de Arquitetura
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Desenhoarquitetura.PNG)

Este desenho de arquitetura contempla a ingestão de dados de uma fonte externa do GCP com finalidade de criar um Datalake no Storage e um Data Warehouse no Big Query para que o time de Business Intelligence consiga tomar as melhores decisões de negócios.

### Cloud Storage

A ferramenta Cloud Storage foi escolhida como Data Lake na nossa arquitetura pois fornece armazenamento dos arquivos ou como um backup de segurança para aqueles que já estão guardados em dispositivos físicos. Isso tudo com a segurança de que seus registros mais importantes não serão perdidos, danificados ou acessados por pessoas sem autorização. O mesmo também oferece Performance otimizada, Infraestrutura virtual ilimitada, ótimo custo-benefício, sincronização instantânea entre todos os aparelhos, alta escalabilidade entre outras.

### Cloud Dataproc
A arquitetura conta com uma camada de ETL no Cloud Dataproc que contemplará o uso do Spark que é uma ferramenta Big Data que tem o objetivo de processar grandes conjuntos de dados de forma paralela e distribuída, além de ser 100 vezes mais rápido pois processa tudo na memória.

### Big Query
O BigQuery foi contemplado na nossa arquitetura porque é um data warehouse totalmente gerenciado e sem servidor que permite análises escalonáveis em petabytes de dados. É uma plataforma como serviço (PaaS) que oferece suporte a consultas usando ANSI SQL. Ele também possui recursos integrados de aprendizado de máquina.

Quando emparelhado com o BI certo como Data Studio, pode ser uma ferramenta poderosa para qualquer negócio. Estas são algumas das principais razões pelas quais você deve considerar o Google BigQuery para suas ferramentas de BI.

### Cloud Functions e Composer 
O fluxo de orquestração da pipeline será gerenciado pelo Cloud Function e Composer, o Cloud Function funcionará como uma Trigger que executará uma Dag no Composer assim que o arquivo CSV chegar no bucket do Cloud Storage com finalidade de reduzir o tempo de carregamento dos dados no Big Query, o Composer terá o trabalho de criar um cluster Dataproc, executar um processo em Spark e desligar a máquina do Dataproc assim que o processamento acabar, seguindo as boas práticas do Google que faz menção sobre criar máquinas no Dataproc de forma preemptiva, além de executar uma task que irá carregar os arquivos processados para o Big Query e chamará uma procedure que atualizará os dados para uma segunda camada TRUSTED com dados Particionados e Clusterizados para melhor desempenho e economia no momento da consulta de dados.

### Cloud IAM
Toda a parte de Segurança será feita pelos papéis padrões do Google Cloud IAM ou Gerenciamento de identidades e acesso permitirá que os administradores decidam quem deve agir sobre os recursos e também abrange a auditoria interna.

### Data Studio 

Google Data Studio foi escolhido porque é uma ferramenta de dashboard do Google altamente personalizável e fácil de usar. É capaz de reunir diversas fontes de dados e extrair informações do Google Analytics, Google Ads, Search Console, YouTube e outras para criar relatórios e painéis informativos totalmente amigáveis.
Assim como os aplicativos no Google Drive, o Data Studio amplia a capacidade de colaboração nas equipes para otimizar a gestão de relatórios de equipes e também entre clientes externos.
Além do fato de ser gratuito – um motivo considerável – o Data Studio possui diversos recursos e vantagens para quem busca transformar dados em informações valiosas para os negócios.

## Escopo do Projeto 
![Desenho Arquitetura](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Escopo_do_Projeto.PNG)

## Premissas
![Desenho Premissas](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/documentos/Premissas.PNG)

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
![pastas_bucket](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/pastas_bucket.PNG) 

Organizei as pastas do Storage por arquivo e ferramenta.

![file_bill_of_materials](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/file_bill_of_materials.PNG) 

Cada pasta de arquivo receberá o arquivo original.

## Cloud Dataproc
![job_pyspark_example](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/job_pyspark.PNG)
![jobs_pyspark_finalizado](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/job_pyspark_finalizado.PNG)

A fase de ETL dos arquivos será execultada em forma de Job no Dataproc com Pyspark, essa execução tem como objetivo a transformação dos dados de CSV para Parquet pois o tipo de dado Parquet oferece muitos benefícios como reduzir o espaço de armazenamento no Cloud Storage, execução mais rápido em determinadas operações, schema automático das tabelas além de ser um dos formatos preferidos do Big Query.  

#### Exemple SPARK
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

## Cloud Functions

#### Como conceder permissões à conta de serviço do Cloud Functions
Para autenticação no IAP, conceda à conta de serviço do Appspot (usada pelo Cloud Functions) o papel Service Account Token Creator. Para fazer isso, execute o comando a seguir na ferramenta de linha de comando gcloud ou no Cloud Shell:
```
gcloud iam service-accounts add-iam-policy-binding \
<b>your-project-id</b>@appspot.gserviceaccount.com \
--member=serviceAccount:<b>your-project-id</b>@appspot.gserviceaccount.com \
--role=roles/iam.serviceAccountTokenCreator
```
Você também precisa conceder o papel composer.user à conta de serviço para que ela possa acionar o DAG:
```
gcloud iam service-accounts add-iam-policy-binding \
<b>your-project-id</b>@appspot.gserviceaccount.com \
--member=serviceAccount:<b>your-project-id</b>@appspot.gserviceaccount.com \
--role=roles/composer.user
```
![id projeto](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/idprojeto.PNG)
#### Mude o parâmetro "your-project-id" para o id do seu projeto.
#### Exemplo:

```
gcloud iam service-accounts add-iam-policy-binding \
fit-union-275813@appspot.gserviceaccount.com \
--member=serviceAccount:fit-union-275813@appspot.gserviceaccount.com \
--role=roles/iam.serviceAccountTokenCreator
```
![service_account_cloud_function](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/service_account_cloud_function.PNG)

#### Como conseguir o ID do cliente
Para criar um token para autenticação no IAP, a função precisa do ID do cliente do proxy que protege o servidor da Web do Airflow. A API Cloud Composer não fornece essas informações diretamente. Em vez disso, faça uma solicitação não autenticada no servidor da Web do Airflow e capture o ID do cliente do URL de redirecionamento. Na amostra de código Python a seguir, demonstramos como conseguir o ID do cliente. Depois de executar esse código na linha de comando ou no Cloud Shell, o ID do cliente será impresso.
```
import google.auth
import google.auth.transport.requests
import requests
import six.moves.urllib.parse

# Authenticate with Google Cloud.
# See: https://cloud.google.com/docs/authentication/getting-started
credentials, _ = google.auth.default(
    scopes=['https://www.googleapis.com/auth/cloud-platform'])
authed_session = google.auth.transport.requests.AuthorizedSession(
    credentials)

project_id = 'YOUR_PROJECT_ID'
location = 'us-east1'
composer_environment = 'YOUR_COMPOSER_ENVIRONMENT_NAME'

environment_url = (
    'https://composer.googleapis.com/v1beta1/projects/{}/locations/{}'
    '/environments/{}').format(project_id, location, composer_environment)
composer_response = authed_session.request('GET', environment_url)
environment_data = composer_response.json()
airflow_uri = environment_data['config']['airflowUri']

# The Composer environment response does not include the IAP client ID.
# Make a second, unauthenticated HTTP request to the web server to get the
# redirect URI.
redirect_response = requests.get(airflow_uri, allow_redirects=False)
redirect_location = redirect_response.headers['location']

# Extract the client_id query parameter from the redirect.
parsed = six.moves.urllib.parse.urlparse(redirect_location)
query_string = six.moves.urllib.parse.parse_qs(parsed.query)
print(query_string['client_id'][0])
```
#### Ordem de execução arquivo Python:
```
1. Abra o Cloud Shell
    1.1. Execute o comando -> sudo vim id_cliente.py 
    1.2. Clique com a tecla -> "i" para entrar no modo de inserção do Vim
    1.3. Cole o programa Python 
    1.4. Mude o project_id = 'YOUR_PROJECT_ID' para o ID de seu projeto
    1.5. Mude o composer_environment = 'YOUR_COMPOSER_ENVIRONMENT_NAME' para o nome do seu ambiente Composer 
    1.6. Aperte a tecla ESC para sair do modo de edição, em seguida rode o comando  -> :wc para salvar o programa .py
    1.7. Rode o código python com o comando -> python id_cliente.py
```
#### Example de saída: 
![cod_python_cloud_function](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/cod_python_cloud_function.PNG)
```
ID do cliente -> 469374234271-soi9m8qvrh9eo2nfrnpblivki4nsth58.apps.googleusercontent.com
```
#### Como criar a função
Crie uma função com os arquivos main.py e requirements.txt mostrados abaixo, preenchendo as primeiras quatro constantes. Consulte Criar uma função. Ative a opção Tentar novamente em caso de falha.

Quando você terminar, a função será parecida com esta imagem:

![example_function](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/gcf-configuration-python.png)

#### main.py
```

from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests

IAM_SCOPE = 'https://www.googleapis.com/auth/iam'
OAUTH_TOKEN_URI = 'https://www.googleapis.com/oauth2/v4/token'

def trigger_dag(data, context=None):
    """Makes a POST request to the Composer DAG Trigger API

    When called via Google Cloud Functions (GCF),
    data and context are Background function parameters.

    For more info, refer to
    https://cloud.google.com/functions/docs/writing/background#functions_background_parameters-python

    To call this function from a Python script, omit the ``context`` argument
    and pass in a non-null value for the ``data`` argument.
    """

    # Fill in with your Composer info here
    # Navigate to your webserver's login page and get this from the URL
    # Or use the script found at
    # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/composer/rest/get_client_id.py
    
    client_id = 'YOUR-CLIENT-ID'
    
    # This should be part of your webserver's URL:
    # {tenant-project-id}.appspot.com
    
    webserver_id = 'YOUR-TENANT-PROJECT'
    
    # The name of the DAG you wish to trigger
    
    dag_name = 'composer_sample_trigger_response_dag'
    
    webserver_url = (
        'https://'
        + webserver_id
        + '.appspot.com/api/experimental/dags/'
        + dag_name
        + '/dag_runs'
    )
    # Make a POST request to IAP which then Triggers the DAG
    make_iap_request(
        webserver_url, client_id, method='POST', json={"conf": data, "replace_microseconds": 'false'})

# This code is copied from
# https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iap/make_iap_request.py
# START COPIED IAP CODE
def make_iap_request(url, client_id, method='GET', **kwargs):
    """Makes a request to an application protected by Identity-Aware Proxy.
    Args:
      url: The Identity-Aware Proxy-protected URL to fetch.
      client_id: The client ID used by Identity-Aware Proxy.
      method: The request method to use
              ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')
      **kwargs: Any of the parameters defined for the request function:
                https://github.com/requests/requests/blob/master/requests/api.py
                If no timeout is provided, it is set to 90 by default.
    Returns:
      The page body, or raises an exception if the page couldn't be retrieved.
    """
    # Set the default timeout, if missing
    if 'timeout' not in kwargs:
        kwargs['timeout'] = 90

    # Obtain an OpenID Connect (OIDC) token from metadata server or using service
    # account.
    google_open_id_connect_token = id_token.fetch_id_token(Request(), client_id)

    # Fetch the Identity-Aware Proxy-protected URL, including an
    # Authorization header containing "Bearer " followed by a
    # Google-issued OpenID Connect token for the service account.
    resp = requests.request(
        method, url,
        headers={'Authorization': 'Bearer {}'.format(
            google_open_id_connect_token)}, **kwargs)
    if resp.status_code == 403:
        raise Exception('Service account does not have permission to '
                        'access the IAP-protected application.')
    elif resp.status_code != 200:
        raise Exception(
            'Bad response from application: {!r} / {!r} / {!r}'.format(
                resp.status_code, resp.headers, resp.text))
    else:
        return resp.text
# END COPIED IAP CODE
```
#### Mudanças 
```
client_id = '{ID do cliente}' # código retornado pelo processo python acima 
```
```
webserver_id = 'https://e73724603f311c57cp-tp.appspot.com' 
```
![web_server_id](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/web_server_id.PNG)
```
dag_name = 'composer-bvs' # Nome da sua DAG
```
![nome_dag](https://github.com/RafaelMiranda775/Desafio_BVS_Engenheiro_De_Dados/blob/main/imagens/nome_dag.PNG)

#### requirements.txt

Atualize seu requirements.txt com as seguintes dependências:

```
requests_toolbelt==0.9.1
google-auth==1.24.0
```
