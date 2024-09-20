CREATE TABLE dim_empleado (
    "EmpID" INT PRIMARY KEY,        -- Clave primaria
    "FirstName" VARCHAR(100),
    "LastName" VARCHAR(100),    
    "Title" VARCHAR(100),
    "Supervisor" VARCHAR(100),
    "ADEmail" VARCHAR(100),
    "BusinessUnit" VARCHAR(100),
    "EmployeeStatus" VARCHAR(50),
    "EmployeeType" VARCHAR(50),
    "PayZone" VARCHAR(50),
    "EmployeeClassificationType" VARCHAR(50),
    "DepartmentType" VARCHAR(100),
    "Division" VARCHAR(100),
    "DOB" DATE,
    "State" VARCHAR(100),
    "JobFunctionDescription" VARCHAR(100),
    "GenderCode" VARCHAR(10),
    "LocationCode" INT,
    "RaceDesc" VARCHAR(50),
    "MaritalDesc" VARCHAR(50)
);

CREATE TABLE fact_empleados (
    "ID_Fact_Empleado" SERIAL PRIMARY KEY,  -- Llave subrogada
    "EmpID" INT NOT NULL,             -- Llave foránea a Dim_Empleado
    "StartDate" DATE,                       -- Fecha de inicio del empleo
    "ExitDate" DATE,                        -- Fecha de salida (si aplicable)
    "TerminationType" VARCHAR(50),          -- Tipo de terminación
    "TerminationDescription" VARCHAR(255),  -- Descripción de la terminación
    "Performance Score" VARCHAR(50),         -- Puntuación de rendimiento
    "Current Employee Rating" INT,  -- Calificación actual del empleado

    FOREIGN KEY ("EmpID") REFERENCES dim_empleado("EmpID") ON DELETE CASCADE -- Relación con dim_empleado
);


CREATE TABLE dim_training_and_development (
    "TrainingProgramID" SERIAL PRIMARY KEY,      -- Identificador único del programa de entrenamiento
    "Training Program Name" VARCHAR(255) NOT NULL -- Nombre del programa de entrenamient
);


CREATE TABLE fact_training_and_development (
    "ID_Fact_Training" SERIAL PRIMARY KEY,   -- Llave primaria para el hecho del entrenamiento
    "Employee ID" INT NOT NULL,                    -- Llave foránea a la tabla dim_empleado
    "TrainingProgramID" INT NOT NULL,        -- Llave foránea a la tabla dim_training_and_development
    "Training Date" DATE,                    -- Fecha del entrenamiento
    "Training Type" VARCHAR(100),             -- Tipo de entrenamiento     
    "Training Outcome" VARCHAR(50),          -- Resultado del entrenamiento (Completado, Parcial, No Completado)
    "Location" VARCHAR(50),                  -- Lugar del entrenamiento 
    "Trainer" VARCHAR(255),                  -- Nombre del entrenador o instructor
    "Training Duration(Days)" VARCHAR(50),   -- Duración del entrenamiento en días
    "Training Cost" DECIMAL(10, 2),          -- Costo del entrenamiento

    FOREIGN KEY ("Employee ID") REFERENCES dim_empleado("EmpID") ON DELETE CASCADE, -- Relación con dim_empleado
    FOREIGN KEY ("TrainingProgramID") REFERENCES dim_training_and_development("TrainingProgramID") ON DELETE CASCADE -- Relación con dim_training_and_development
);


CREATE TABLE dim_recruitment_data (
    "Applicant ID" INT PRIMARY KEY,       -- Identificador único del candidato
    "First Name" VARCHAR(255),        -- Primer nombre del candidato
    "Last Name" VARCHAR(255),         -- Apellido del candidato
    "Gender" VARCHAR(50),             -- Género del candidato
    "Date of Birth" DATE,             -- Fecha de nacimiento del candidato
    "Phone Number" VARCHAR(50),       -- Número de teléfono del candidato
    "Email" VARCHAR(255),               -- Correo electrónico del candidato
    "Address" VARCHAR(255),             -- Dirección del candidato
    "City" VARCHAR(100),                -- Ciudad del candidato
    "State" VARCHAR(100),               -- Estado del candidato
    "Zip Code" VARCHAR(50),              -- Código postal del candidato
    "Country" VARCHAR(100),             -- País del candidato
    "Education Level" VARCHAR(100)       -- Nivel de educación del candidato
);


CREATE TABLE dim_jobs_recruitment_data (
    "JobID" SERIAL PRIMARY KEY,         -- Identificador único del trabajo
    "Job Title" VARCHAR(255)             
);

CREATE TABLE fact_recruitment_data (
    "RecruitmentID" SERIAL PRIMARY KEY,     -- Identificador único para el hecho de reclutamiento
    "Applicant ID" INT ,                    -- Llave foránea a Dim_Applicant
    "JobID" INT ,                           -- Llave foránea a Dim_Job
    "Application Date" DATE,                 -- Fecha de la aplicación
    "Years of Experience" INT,                -- Años de experiencia del candidato
    "Desired Salary" DECIMAL(10, 2),          -- Salario deseado por el candidato
    "Status" VARCHAR(50),                   -- Estado de la aplicación (Submitted, Rejected, etc.)
     FOREIGN KEY ("Applicant ID") REFERENCES dim_recruitment_data("Applicant ID") ON DELETE CASCADE, -- Relación con dim_recruitment_data
    FOREIGN KEY ("JobID") REFERENCES dim_jobs_recruitment_data("JobID") ON DELETE CASCADE -- Relación con dim_jobs_recruitment_data
);


CREATE TABLE fact_employee_engagement_survey_data (
    "SurveyID" SERIAL PRIMARY KEY,     -- Identificador único de la encuesta
    "Employee ID" INT ,                -- Llave foránea a la tabla de empleados
    "Survey Date" DATE ,             -- Fecha
    "Engagement Score" INT,    -- Puntaje de compromiso del empleado
    "Satisfaction Score" INT,  -- Puntaje de satisfacción del empleado
    "Work-Life Balance Score" INT, -- Puntaje de equilibrio entre vida personal y laboral
    
      FOREIGN KEY ("Employee ID") REFERENCES dim_empleado("EmpID") ON DELETE CASCADE -- Relación con dim_empleado
);


