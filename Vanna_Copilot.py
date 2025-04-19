from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

class MyVanna(ChromaDB_VectorStore,Ollama):
    
    def __init__(self,config=None):
        ChromaDB_VectorStore.__init__(self,config=config)
        Ollama.__init__(self,config=config)
        
vn=MyVanna(config={'model':"llama3"})
vn.connect_to_postgres(host="localhost",port=5432,dbname="postgres",user="postgres",password="pg1234")
information_schema=vn.run_sql("SELECT * from INFORMATION_SCHEMA.COLUMNS")
plan=vn.get_training_plan_generic(information_schema)
vn.train(plan=plan)
vn.train(sql=""" CREATE TABLE jobs_data
(
    work_year bigint,
    job_title character varying,
    job_category character varying,
    salary_currency character varying,
    salary bigint,
    salary_in_usd bigint,
    employee_residence character varying,
    experience_level character varying,
    employment_type character varying,
    work_setting character varying,
    company_location character varying,
    company_size character
)""")
vn.train(sql="SELECT * FROM jobs_data")
vn.train(documentation="The jobs_data table contains information about job postings, including work year, job title, salary, and company location.")
vn.generate_sql("what is the highest salary in the jobs_data table")
vn.ask("what is the highest salary in the jobs_data table")

#Flask APP
vn.ask("what are different experience levels from jobs_data",allow_llm_to_see_data=True)
from vanna.flask import VannaFlaskApp
app=VannaFlaskApp(vn,allow_llm_to_see_data=True)
app.run()

