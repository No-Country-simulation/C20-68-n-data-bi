import sqlalchemy
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine,text


#EMPLEADOS
df_empleados_db = pd.read_csv('C:/Users/ASUS/Documents/NoCountry/datos/employee_data.csv', sep=';')

# Arreglar Formato de Fechas
df_empleados_db["StartDate"] = pd.to_datetime(df_empleados_db["StartDate"], format="%d-%b-%y")
df_empleados_db["ExitDate"] = pd.to_datetime(df_empleados_db["ExitDate"], format="%d-%b-%y")
df_empleados_db["DOB"] = pd.to_datetime(df_empleados_db["DOB"], format="%d/%m/%Y")

# Quitar espacios en blanco de las columnas de categoria 
df_empleados_db["FirstName"] = df_empleados_db["FirstName"].str.strip()
df_empleados_db["LastName"] = df_empleados_db["LastName"].str.strip()
df_empleados_db["Title"] = df_empleados_db["Title"].str.strip()
df_empleados_db["Supervisor"] = df_empleados_db["Supervisor"].str.strip()
df_empleados_db["DepartmentType"] = df_empleados_db["DepartmentType"].str.strip()
df_empleados_db["Division"] = df_empleados_db["Division"].str.strip()
df_empleados_db["JobFunctionDescription"] = df_empleados_db["JobFunctionDescription"].str.strip()
df_empleados_db.replace(['NaN', 'N/A', 'NA', 'n/a', 'n.a.', 'N#A', 'n#a', '?'], 'other', inplace=True)



# Dimensión del empleado
df_dim_empleado = df_empleados_db[['EmpID', 'FirstName', 'LastName','Title', 
                                   'Supervisor', 'ADEmail', 'BusinessUnit', 
                                   'EmployeeStatus','EmployeeType','PayZone',
                                  'EmployeeClassificationType', 'DepartmentType', 
                                  'Division','DOB','State', 'JobFunctionDescription', 'GenderCode', 'LocationCode', 
                                   'RaceDesc', 'MaritalDesc'
                                 ]]
# Tabla de hechos de empleados
df_fact_empleados = df_empleados_db[['EmpID', 'StartDate', 'ExitDate', 
                                     'TerminationType', 'TerminationDescription',
                                     'Performance Score', 'Current Employee Rating'
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
    connection.execute(text("TRUNCATE TABLE dim_empleado CASCADE;"))
    connection.execute(text("TRUNCATE TABLE fact_empleados CASCADE;"))
    

# Insertar los nuevos datos
df_dim_empleado.to_sql('dim_empleado', engine, if_exists='append', index=False)

df_fact_empleados.to_sql('fact_empleados', engine, if_exists='append', index=False)