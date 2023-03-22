from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from models.dag_noticia import AbstractNoticias



DAG_NAME = 'dag_request_api'
DAG_DESCRIPTION = 'DAG para fazer requisição tipo post em uma api'
DEFAULT_ARGS = {
    'owner': 'Otiliano Junior',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 20),
    'email': ['seu_email@exemplo.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
}
SCHEDULE_INTERVAL = timedelta(days=1)

urls = {'url_1': 'https://www.bbc.com/news/world-65035041',
        'url_2': 'https://oantagonista.uol.com.br/brasil/mais-medicos-tenta-atrair-endividados-do-fies/',
        'url_3': 'https://www.bbc.com/news/business-59212992',
        'url_4': 'https://www1.folha.uol.com.br/poder/2023/03/pf-faz-operacao-contra-grupo-que-planejava-atacar-autoridades-moro-era-um-dos-alvos.shtml',
        'url_5': 'https://tab.uol.com.br/noticias/redacao/2023/03/22/refugiadas-no-brasil-ucranianas-vao-voltar-para-casa-mesmo-com-a-guerra.htm'
        }


dag = DAG(DAG_NAME,
          description=DAG_DESCRIPTION,
          default_args=DEFAULT_ARGS,
          schedule_interval=SCHEDULE_INTERVAL,
          concurrency=1)

start_operator = EmptyOperator(task_id='start', dag=dag)

requisicao_site_operators = []
for key, url in urls.items():
    task_id = f'requisicao_site_{key}'
    requisicao_site_operator = PythonOperator(
        task_id=task_id,
        python_callable=AbstractNoticias.requisicao_site,
        op_args=[url],
        dag=dag)
    requisicao_site_operators.append(requisicao_site_operator)

trasforma_dados_operator = PythonOperator(
    task_id='trasforma_dados',
    python_callable=AbstractNoticias.trasforma_dados,
    op_args=[r.output for r in requisicao_site_operators],
    provide_context=True, dag=dag)

salva_mongo_operador = PythonOperator(
    task_id='insere_no_mongodb',
    python_callable=AbstractNoticias.salva_mongo,
    op_args=[trasforma_dados_operator.output],
    provide_context=True,
    dag=dag
)

start_operator >> requisicao_site_operators >> trasforma_dados_operator >> salva_mongo_operador
