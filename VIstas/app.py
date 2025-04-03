from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = "secreta"  

FASTAPI_URL = "http://127.0.0.1:5001"

@app.route('/')
def home():
    return render_template('registro.html')

@app.route('/consulta')
def consulta():
    return redirect(url_for('get_usuarios'))

@app.route('/usuariosFastAPI', methods=['POST'])
def post_usuario():
    try:
        usuarioNuevo = {
            "name": request.form['txtNombre'],
            "age": int(request.form['txtEdad']),
            "email": request.form['txtCorreo']
        }

        response = requests.post(f"{FASTAPI_URL}/usuarios", json=usuarioNuevo)
        
        if response.status_code == 200 or response.status_code == 201:
            flash("Usuario guardado correctamente", "success")
        else:
            flash(f"Error al guardar usuario: {response.json().get('detail', 'Error desconocido')}", "danger")
        
        return redirect(url_for('home'))
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "No se pudo conectar con la API", "detalle": str(e)}), 500

@app.route('/ConsultaUsuarios', methods=['GET'])
def get_usuarios():
    try:
        response = requests.get(f"{FASTAPI_URL}/todosUsuario")
        response.raise_for_status()
        usuarios = response.json()
        return render_template('consulta.html', usuarios=usuarios)
    except requests.exceptions.RequestException as e:
        flash(f"Error al obtener usuarios: {str(e)}", "danger")
        return render_template('consulta.html', usuarios=[])

@app.route('/actualizarUsuario/<int:id>', methods=['GET', 'POST'])
def actualizar_usuario(id):
    if request.method == 'GET':
        try:
            response = requests.get(f"{FASTAPI_URL}/todosUsuario/{id}")
            response.raise_for_status()
            usuario = response.json()
            return render_template('editar_usuario.html', usuario=usuario)
        except requests.exceptions.RequestException as e:
            flash(f"Error al obtener usuario: {str(e)}", "danger")
            return redirect(url_for('get_usuarios'))
    
    elif request.method == 'POST':
        try:
            datos_actualizados = {
                "name": request.form['txtNombre'],
                "age": int(request.form['txtEdad']),
                "email": request.form['txtCorreo']
            }
            
            response = requests.put(f"{FASTAPI_URL}/updateUsuario/{id}", json=datos_actualizados)
            
            if response.status_code == 200:
                flash("Usuario actualizado correctamente", "success")
            else:
                flash(f"Error al actualizar usuario: {response.json().get('detail', 'Error desconocido')}", "danger")
            
            return redirect(url_for('get_usuarios'))
        
        except requests.exceptions.RequestException as e:
            flash(f"Error al conectar con la API: {str(e)}", "danger")
            return redirect(url_for('get_usuarios'))

@app.route('/eliminarUsuario/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    try:
        response = requests.delete(f"{FASTAPI_URL}/deleteUsuario/{id}")
        
        if response.status_code == 200:
            flash("Usuario eliminado correctamente", "success")
        else:
            flash(f"Error al eliminar usuario: {response.json().get('detail', 'Error desconocido')}", "danger")
        
        return redirect(url_for('get_usuarios'))
    
    except requests.exceptions.RequestException as e:
        flash(f"Error al conectar con la API: {str(e)}", "danger")
        return redirect(url_for('get_usuarios'))

if __name__ == '__main__':
    app.run(debug=True, port=8002)