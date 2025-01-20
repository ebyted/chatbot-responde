import sqlite3

# Conectar a la base de datos (asegúrate de que 'chatbot.bd' esté en el mismo directorio)
conn = sqlite3.connect('chatbot.bd')
cursor = conn.cursor()

# Consultar todos los registros de la tabla 'respuestas'
cursor.execute("SELECT * FROM respuestas")

# Obtener todos los resultados
registros = cursor.fetchall()

# Imprimir los resultados
if registros:
    for row in registros:
        print(f"Palabra clave: {row[0]}, Respuesta: {row[1]}")
else:
    print("No hay registros en la tabla 'respuestas'.")

# Cerrar la conexión
conn.close()
