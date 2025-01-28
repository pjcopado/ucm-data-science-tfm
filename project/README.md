# SQL Query Generator

Este proyecto utiliza un modelo de lenguaje natural preentrenado para interpretar preguntas en lenguaje natural y generar consultas SQL. También incluye validación de las consultas generadas y permite iteraciones automáticas para corregir errores.

---

## **Estructura del Proyecto**

```plaintext
project/
├── main.py                              # Archivo principal, punto de entrada del proyecto
├── prompts/
│   ├── prompt_generate_sql.txt          # Plantilla para generar las consultas SQL
│   ├── prompt_generate_sql_error.txt    # Plantilla para generar las consultas SQL de reintento
├── modules/
│   ├── __init__.py                      #
│   ├── prompt_loader.py                 # Carga y manejo de archivos de prompts
│   ├── posgres.py                       # Conexión con posgres
│   ├── sql_generator.py                 # Validación y ejecución del modelo de consultas SQL
├── models/
│   ├── llama-3-sqlcoder-8b/             # Directorio del modelo preentrenado (tokenizador y modelo)
└── README.md                            # Documentación del proyecto

.\.venv\Scripts\Activate