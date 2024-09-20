import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine,text

#ENCUESTAS
df_encuesta_db = pd.read_csv('C:/Users/ASUS/Documents/NoCountry/datos/employee_engagement_survey_data.csv', sep=',')

# Arreglar Formato de Fechas
df_encuesta_db["Survey Date"] = pd.to_datetime(df_encuesta_db["Survey Date"], format="%d-%m-%Y")

# Quitar espacios en blanco de las columnas de categoria 
df_encuesta_db.replace(['NaN', 'N/A', 'NA', 'n/a', 'n.a.', 'N#A', 'n#a', '?'], 'other', inplace=True)


# Tabla de hechos de encuesta
df_fact_encuesta = df_encuesta_db[['Employee ID', 'Survey Date', 'Engagement Score', 
                                     'Satisfaction Score', 'Work-Life Balance Score'
                                    ]]


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
    connection.execute(text("TRUNCATE TABLE fact_employee_engagement_survey_data CASCADE;"))
    


df_fact_encuesta.to_sql('fact_employee_engagement_survey_data', engine, if_exists='append', index=False)