from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Cargar el modelo entrenado
modelo = joblib.load("modelo_lluvia.pkl")

@app.route('/predecir', methods=['POST'])
def predecir():
    datos = request.get_json()

    # Obtener variables desde Lambda (o cualquier cliente)
    humedad = datos.get("humedad", 0)
    presion = datos.get("presion", 1010)
    temperatura = datos.get("temperatura", 20)
    visibilidad = datos.get("visibilidad", 10)
    viento = datos.get("viento", 2)
    nubes = datos.get("nubes", 0)
    descripcion = datos.get("descripcion", "")

    # Armar el vector de entrada en el orden del entrenamiento
    entrada = np.array([[humedad, presion, temperatura, visibilidad, viento]])

    # Hacer la predicción
    prediccion = modelo.predict(entrada)[0]

    #Condiciones extremadamente secas y despejadas
    if nubes == 0 and descripcion  == "clear sky":
    	prediccion = 0



    return jsonify({
        "lluvia_probable": bool(prediccion),
        "input": {
            "humedad": humedad,
            "presion": presion,
            "temperatura": temperatura,
            "visibilidad": visibilidad,
            "viento": viento
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
