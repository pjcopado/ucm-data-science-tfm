-- Crear la base de datos si no existe
CREATE DATABASE evaluation_log;

-- Conectar a la base de datos
\c evaluation_log;

-- Habilitar la extensión vector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE logs (
    id uuid PRIMARY KEY,                                -- Identificador único para cada log
    user_input TEXT NOT NULL,                             -- Texto de la consulta original
    user_input_embedding vector(384),                     -- Embedding del input del usuario (dimensión ajustable)
    query TEXT NOT NULL,                                  -- Query generada por el LLM
    query_embedding vector(384),                          -- Embedding de la query generada
    is_correct BOOLEAN,                                   -- Si la query es correcta o no
    error_message TEXT,
    execution_time FLOAT,                                 -- Tiempo de ejecución en milisegundos
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()  -- Fecha y hora de creación del log
);
