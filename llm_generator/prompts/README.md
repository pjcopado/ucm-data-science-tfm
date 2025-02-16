### **Partes del prompt**

1. **`<|begin_of_text|>`**

   - **Significado:** Marca el inicio del texto del input.
   - **Uso:** Es un token especial que indica al modelo que empieza un nuevo bloque de texto.

2. **`<|start_header_id|>user<|end_header_id|>`**

   - **Significado:** Identifica que el contenido posterior corresponde a un input del usuario.
   - **Uso:** Este encabezado etiqueta el bloque como la pregunta o instrucción dada por el usuario.

3. **`Generate a SQL query to answer this question: {user_question}`**

   - **Significado:** Solicita al modelo que genere una consulta SQL para responder la pregunta formulada por el usuario.
   - **Uso:** Aquí, `{user_question}` se sustituye con la pregunta real en lenguaje natural. Ejemplo: `"What is the total revenue from last month?"`.

4. **`{instructions}`**

   - **Significado:** Permite proporcionar instrucciones adicionales para guiar la generación de la consulta.
   - **Uso:** Por ejemplo, podrías incluir detalles sobre filtros o limitaciones específicas:
     - `"Include only orders with status 'completed'"`.
     - Si no necesitas instrucciones adicionales, este campo puede omitirse.

5. **`DDL statements:`**

   - **Significado:** Señala que las definiciones de las tablas (DDL: Data Definition Language) se especifican a continuación.
   - **Uso:** Esto le da al modelo el contexto sobre las tablas y columnas en la base de datos para generar una consulta coherente. Ejemplo:
     ```plaintext
     CREATE TABLE orders (
         order_id INT,
         customer_id INT,
         total_amount DECIMAL,
         order_date DATE
     );
     ```

6. **`{create_table_statements}`**

   - **Significado:** Aquí van las declaraciones DDL reales que describen la estructura de las tablas relevantes.
   - **Uso:** Este bloque debe incluir definiciones completas de tablas que el modelo necesita para entender cómo están organizados los datos.

7. **`<|eot_id|>`**

   - **Significado:** Marca el final del bloque de texto proporcionado por el usuario.
   - **Uso:** Es un token especial que ayuda al modelo a diferenciar entre el input del usuario y la respuesta que debe generar.

8. **`<|start_header_id|>assistant<|end_header_id|>`**

   - **Significado:** Identifica que lo que sigue es la respuesta generada por el asistente (el modelo).
   - **Uso:** Este encabezado etiqueta el bloque como la salida esperada (la consulta SQL).

9. **`The following SQL query best answers the question {user_question}:`**

   - **Significado:** Introduce la consulta SQL que responde mejor la pregunta proporcionada.
   - **Uso:** `{user_question}` se repite aquí para contextualizar la respuesta. Esto ayuda a hacer el output más interpretable.

10. **`sql`**

    - **Significado:** Define el bloque de código como SQL.
    - **Uso:** Indica que lo que sigue es un código SQL válido. Esto es útil si estás utilizando un editor de texto o herramientas que pueden reconocer sintaxis SQL.

11. **Consulta SQL generada**
    - **Significado:** Es la consulta generada por el modelo basada en el input proporcionado.
    - **Uso:** Este es el resultado final que puedes ejecutar en tu base de datos.

---

### **Ejemplo completo**

#### Input del prompt:

````plaintext
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Generate a SQL query to answer this question: 'What is the total revenue for completed orders?'
Include only orders from the last month.
DDL statements:
CREATE TABLE orders (
    order_id INT,
    customer_id INT,
    total_amount DECIMAL,
    status VARCHAR(20),
    order_date DATE
);<|eot_id|><|start_header_id|>assistant<|end_header_id|>
The following SQL query best answers the question 'What is the total revenue for completed orders?':
```sql
SELECT SUM(total_amount) AS total_revenue
FROM orders
WHERE status = 'completed' AND order_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month';
````
