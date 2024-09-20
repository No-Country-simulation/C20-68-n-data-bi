import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine,text


#ENTRENAMIENTO
df_entrenamiento_db = pd.read_csv('C:/Users/ASUS/Documents/NoCountry/datos/training_and_development_data.csv', sep=',')

# Asegúrate de usar el nombre correcto basado en lo que imprime el paso anterior
df_entrenamiento_db.columns = df_entrenamiento_db.columns.str.strip()  # Elimina espacios adicionales en los nombres de las columnas


# Arreglar Formato de Fechas
df_entrenamiento_db["Training Date"] = pd.to_datetime(df_entrenamiento_db["Training Date"], format="%d-%b-%y")

# Quitar espacios en blanco de las columnas de categoria 
df_entrenamiento_db["Training Program Name"] = df_entrenamiento_db["Training Program Name"].str.strip()
df_entrenamiento_db["Training Type"] = df_entrenamiento_db["Training Type"].str.strip()
df_entrenamiento_db["Training Outcome"] = df_entrenamiento_db["Training Outcome"].str.strip()
df_entrenamiento_db["Location"] = df_entrenamiento_db["Location"].str.strip()
df_entrenamiento_db["Trainer"] = df_entrenamiento_db["Trainer"].str.strip()
df_entrenamiento_db.replace(['NaN', 'N/A', 'NA', 'n/a', 'n.a.', 'N#A', 'n#a', '?'], 'other', inplace=True)



# Dimensión del entrenamiento
df_dim_training_and_development = df_entrenamiento_db[['Training Program Name']].drop_duplicates()
# Tabla de hechos del entrenamiento (sin TrainingProgramID)
df_fact_training_and_development = df_entrenamiento_db[['Employee ID', 'Training Date', 'Training Type','Training Outcome', 
                                   'Location', 'Trainer',
                                     'Training Duration(Days)', 'Training Cost','Training Program Name'
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
    connection.execute(text("TRUNCATE TABLE dim_training_and_development CASCADE;"))
    connection.execute(text("TRUNCATE TABLE fact_training_and_development CASCADE;"))
    

# Insertar los datos de la dimensión de entrenamiento
df_dim_training_and_development.to_sql('dim_training_and_development', engine, if_exists='append', index=False)

# 1. Recuperar todos los "Training Program Name" y "TrainingProgramID" en una sola consulta
query = """
    SELECT "TrainingProgramID", "Training Program Name"
    FROM dim_training_and_development;
"""
df_training_programs = pd.read_sql(query, engine)

# 2. Hacer un merge entre el DataFrame de origen y los datos de la consulta
df_fact_training_and_development = pd.merge(
    df_fact_training_and_development,          # DataFrame original
    df_training_programs,                      # DataFrame con los programas de entrenamiento y sus IDs
    how='left',                                # Dejar todas las filas del DataFrame original
    left_on='Training Program Name',           # Columna en el DataFrame original
    right_on='Training Program Name'           # Columna en el DataFrame de programas
)


# Crear un nuevo DataFrame con solo las columnas que deseas insertar
df_fact_training_with_program_id = df_fact_training_and_development[[
    'Employee ID', 'TrainingProgramID', 'Training Date', 'Training Type',
    'Training Outcome', 'Location', 'Trainer', 'Training Duration(Days)', 'Training Cost'
]]

# Insertar los datos en la tabla 'fact_training_and_development' sin la columna 'Training Program Name'
df_fact_training_with_program_id.to_sql('fact_training_and_development', engine, if_exists='append', index=False)

