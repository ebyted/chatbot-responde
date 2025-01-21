from flask import Flask, render_template, request
import sqlite3
import os
import nltk
from nltk.tokenize import word_tokenize

# Configurar el directorio para los datos de NLTK y descargar los recursos necesarios
nltk.data.path.append('./nltk_data')
nltk.download('punkt', download_dir='./nltk_data')

app = Flask(__name__)

# Ruta de la base de datos
DATABASE = 'chatbot.bd'

# Función para inicializar la base de datos si no existe la tabla respuestas
def init_db():
    """Crea la tabla respuestas si no existe."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS respuestas (
        palabra_clave TEXT PRIMARY KEY,
        respuesta TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Inicializa la base de datos
init_db()

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        # Tokenizar la entrada del usuario
        tokens = word_tokenize(user_input.lower())
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        response = "Lo siento, no entiendo esa palabra clave."
        
        # Buscar una respuesta para cada token en la base de datos
        for token in tokens:
            cursor.execute("SELECT respuesta FROM respuestas WHERE palabra_clave = ?", (token,))
            result = cursor.fetchone()
            if result:
                response = result[0]
                break  # Detener la búsqueda si se encuentra una respuesta
        conn.close()
        
        return render_template('chat.html', user_input=user_input, response=response)
    return render_template('chat.html')

@app.route('/configuracion', methods=['GET', 'POST'])
def configuracion():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if request.method == 'POST':
        palabra_clave = request.form.get('palabra_clave')
        respuesta = request.form.get('respuesta')
        if 'add' in request.form:
            cursor.execute("INSERT OR IGNORE INTO respuestas (palabra_clave, respuesta) VALUES (?, ?)", 
                           (palabra_clave.lower(), respuesta))
        elif 'delete' in request.form:
            cursor.execute("DELETE FROM respuestas WHERE palabra_clave = ?", (palabra_clave.lower(),))
        elif 'update' in request.form:
            cursor.execute("UPDATE respuestas SET respuesta = ? WHERE palabra_clave = ?", 
                           (respuesta, palabra_clave.lower()))
        conn.commit()

    cursor.execute("SELECT * FROM respuestas")
    respuestas = cursor.fetchall()
    conn.close()

    return render_template('configuracion.html', respuestas=respuestas)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
