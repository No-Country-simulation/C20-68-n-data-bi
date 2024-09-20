# C20-68-n-data-bi
# 📊 Análisis de Retención de Empleados

## 🏢 Industria o Rubro
**Recursos Humanos**

## 📄 Descripción
Este proyecto se centra en el análisis de datos de recursos humanos de una empresa para identificar factores que influyen en la retención de empleados y desarrollar estrategias de retención efectivas 

 Realizar este tipo de análisis se puede identificar patrones y factores que influyen en la retención de empleados en una empresa. Una vez identificados estos factores, se pueden desarrollar estrategias como:
 - Programas de desarrollo para empleados con puntajes de desempeño bajos.
 - Beneficios y políticas de flexibilidad para empleados con bajas puntuaciones en satisfacción o equilibrio vida/trabajo.
 - Planes de carrera para empleados más jóvenes para aumentar su permanencia en la empresa.
 - Políticas de contratación más enfocadas en tipos de empleo que garanticen una mayor retención a largo plazo.

<div align="center">
  <img src="retencion.png" alt="Proceso de Análisis de Retención de Empleados">
</div>
- DataWareHouse Modelo Estrella
<div align="center">
  <img src="modeloestrella.png" alt="Modelo Estrella">
</div>


## 👥 Team leader 
- **Andrés G Velasquez** - Team leader


## 👥 Colaboradores

| Integrantes | Rol | Contacto
|------------|------------|------------|
| [Alejandra Moreno Vallejo](https://github.com/alejamorenovallejo) | ![Data Engineer](https://img.shields.io/badge/Data%20Engineer-black?style=for-the-badge&color=%2384b6f4) | [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/alejamorenovallejo) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alejandra-moreno-vallejo-4b1926138/)

## 💻 Tecnologías
- Python (Proceso de ETL)
  - Pandas 
  - SQLAlchemy 
- PostgreSQL (Para Nuestro DataWareHouse)
  - La base de datos fue desplegada en Render (https://dashboard.render.com/)
- Power BI (Dashboard)

## 🤖 Estructura del proyecto 
* 1_Source: Contiene los datos utilizados en el proyecto.
* 2_ETL: Contiene los archivos pyhton donde se realiza proceso de extraccion, limpieza y carga al datawarehouse realizado para el proyecto que se encuentra publicado en render en una base de datos postgresql
* 3_DataWareHouse: Contiene la estructura del DatawareHouse en sql.
* 4_DashboardPowerBI : Contiene el dashboard correspondiente a nuestro análisis

<div align="center">
  <img src="No_Country.jpg" alt="No Country">
</div>



## 📝 Instrucciones para obtener el proyecto

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/No-Country-simulation/C20-68-n-data-bi.git
