import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine,text


#APLICACIONES
df_aplicacion_db = pd.read_csv('C:/Users/ASUS/Documents/NoCountry/datos/recruitment_data.csv', sep=',')

# Asegúrate de usar el nombre correcto basado en lo que imprime el paso anterior
df_aplicacion_db.columns = df_aplicacion_db.columns.str.strip()  # Elimina espacios adicionales en los nombres de las columnas


# Arreglar Formato de Fechas
df_aplicacion_db["Application Date"] = pd.to_datetime(df_aplicacion_db["Application Date"], format="%d-%b-%y")
df_aplicacion_db["Date of Birth"] = pd.to_datetime(df_aplicacion_db["Date of Birth"], format="%d-%m-%Y")

# Quitar espacios en blanco de las columnas de categoria 
df_aplicacion_db["First Name"] = df_aplicacion_db["First Name"].str.strip()
df_aplicacion_db["Last Name"] = df_aplicacion_db["Last Name"].str.strip()
df_aplicacion_db["Gender"] = df_aplicacion_db["Gender"].str.strip()
df_aplicacion_db["Email"] = df_aplicacion_db["Email"].str.strip()
df_aplicacion_db["City"] = df_aplicacion_db["City"].str.strip()
df_aplicacion_db["State"] = df_aplicacion_db["State"].str.strip()
df_aplicacion_db["Country"] = df_aplicacion_db["Country"].str.strip()
df_aplicacion_db["Education Level"] = df_aplicacion_db["Education Level"].str.strip()
df_aplicacion_db["Job Title"] = df_aplicacion_db["Job Title"].str.strip()
df_aplicacion_db["Status"] = df_aplicacion_db["Status"].str.strip()
df_aplicacion_db.replace(to_replace=r'#', value='', regex=True, inplace=True)


df_aplicacion_db.replace(['NaN', 'N/A', 'NA', 'n/a', 'n.a.', 'N#A', 'n#a', '?'], 'other', inplace=True)


# Dimensión del jobs
df_dim_jobs_recruitment_data = df_aplicacion_db[['Job Title']].drop_duplicates()

# Dimension de Aplicacion
df_dim_recruitment_data = df_aplicacion_db[['Applicant ID','First Name','Last Name','Gender','Date of Birth','Phone Number'
                                            ,'Email','Address','City','State','Zip Code','Country','Education Level']]

#Fact de Aplicacion (sin JobId)
df_fact_recruitment_data = df_aplicacion_db[['Applicant ID','Job Title','Application Date','Years of Experience','Desired Salary','Status']]

#Conectar a base de datos prostgress
# Datos de conexión
usuario = 'nocountryetl_user'
password = 'NyAC5hx3QP86jc4W42kl78HP22twppIN'
host = 'dpg-crfnlbjv2p9s73a07b3g-a.oregon-postgres.render.com'
port = '5432'  # usualmente es 5432 para PostgreSQL
db_name = 'nocountryetl'

# Crear la conexión con PostgreSQL
engine = create_engine(f'postgresql://{usuario}:{password}@{host}:{port}/{db_name}')
  
# Borrar datos en las tablas sin afectar la estructura
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE dim_jobs_recruitment_data CASCADE;"))
    connection.execute(text("TRUNCATE TABLE dim_recruitment_data CASCADE;"))
    connection.execute(text("TRUNCATE TABLE fact_recruitment_data CASCADE;"))
    

# Insertar los datos de la dimensión de jobs
df_dim_jobs_recruitment_data.to_sql('dim_jobs_recruitment_data', engine, if_exists='append', index=False)

# Insertar los datos de la dimensión de aplicacion
df_dim_recruitment_data.to_sql('dim_recruitment_data', engine, if_exists='append', index=False)


# 1. Recuperar todos los "Job Title" y "JobID" en una sola consulta
query = """
    SELECT "JobID", "Job Title"
    FROM dim_jobs_recruitment_data;
"""
df_jobs_recruitment_data = pd.read_sql(query, engine)

# 2. Hacer un merge entre el DataFrame de origen y los datos de la consulta
df_fact_recruitment_data = pd.merge(
    df_fact_recruitment_data,                  # DataFrame original
    df_jobs_recruitment_data,                  # DataFrame con los trabajos y sus IDs
    how='left',                                # Dejar todas las filas del DataFrame original
    left_on='Job Title',           # Columna en el DataFrame original
    right_on='Job Title'           # Columna en el DataFrame de jobs
)


# Crear un nuevo DataFrame con solo las columnas que deseas insertar
df_fact_recruitment_data_with_job_id = df_fact_recruitment_data[[
    'Applicant ID', 'JobID', 'Application Date', 'Years of Experience',
    'Desired Salary', 'Status'
]]

# Insertar los datos en la tabla 'fact_recruitment_data' sin la columna 'Job Title'
df_fact_recruitment_data_with_job_id.to_sql('fact_recruitment_data', engine, if_exists='append', index=False)





