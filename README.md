# 🌍 Climate Monitoring Prototype using AWS & OpenWeather

Este repositorio contiene un prototipo funcional de un sistema de monitoreo climático en tiempo real. Está diseñado para recolectar, procesar, almacenar y visualizar datos meteorológicos utilizando servicios de AWS, Python, Streamlit y modelos de Machine Learning.

---

## 🎯 Objetivo

El objetivo de este prototipo es demostrar una solución mínima viable que:

- Recolecta datos del clima desde la API pública de OpenWeather.
- Ejecuta un modelo de predicción de lluvia basado en aprendizaje automático.
- Almacena la información procesada en una base de datos en la nube.
- Permite visualizar y explorar los datos a través de un dashboard interactivo.

---

## 🧱 Arquitectura del Sistema

![image](https://github.com/user-attachments/assets/a4106e4e-da5e-418a-a3b3-be2cc3364b2f)


**Componentes:**

- **OpenWeather API**: Fuente de datos meteorológicos.
- **AWS Lambda**: Obtiene y envía los datos a una EC2 que ejecuta un modelo de predicción.
- **EC2 - Modelo ML**: Predice probabilidad de lluvia con `scikit-learn` y devuelve la respuesta.
- **Amazon DynamoDB**: Almacena los registros procesados.
- **EC2 - Dashboard Streamlit**: Visualiza los datos históricos y genera predicciones básicas.

---

## 🧠 Tecnologías y Servicios Utilizados

| Tecnología       | Uso Principal                          |
|------------------|----------------------------------------|
| Python 3.9       | Lógica de backend y ML                 |
| Streamlit        | Dashboard web para visualización       |
| Flask            | Microservicio REST del modelo ML       |
| Scikit-learn     | Entrenamiento y ejecución del modelo   |
| AWS Lambda       | Orquestación de recolección de datos   |
| AWS EC2          | Hospedaje del modelo ML y dashboard    |
| AWS DynamoDB     | Base de datos NoSQL para almacenamiento|
| OpenWeather API  | Fuente externa de datos climáticos     |

---

## 📁 Estructura del Repositorio

```
climate-monitoring-prototype/
│
├── model-ec2/
│   ├── app.py               # API Flask que ejecuta el modelo
│   ├── entrenamiento.py     # Entrena y guarda el modelo
│   └── modelo_lluvia.pkl    # Modelo entrenado (binario)
│
├── dashboard-ec2/
│   ├── dashboard.py         # Aplicación Streamlit
│   └── datos_clima.csv      # Datos históricos para visualización
│
├── diagrams/
│   └── arquitectura-prototipo.png  # Diagrama del sistema
│
└── README.md
```

---

## ⚙️ Instalación y Ejecución

### 🔧 Requisitos previos

- Cuenta en AWS con permisos para EC2, Lambda y DynamoDB.
- Python 3.9 instalado en ambas EC2.
- Claves de API de OpenWeather.

---

### 📦 1. Modelo de Predicción (EC2 #1)

```bash
# Entrena el modelo
cd model-ec2
pip install -r requirements.txt  # incluye flask, scikit-learn, pandas, joblib
python entrenamiento.py

# Ejecuta la API Flask
python app.py
# Corre en http://<IP_EC2>:5000/predecir
```

---

### 📦 2. Dashboard Visual (EC2 #2)

```bash
cd dashboard-ec2
pip install streamlit pandas

# Asegúrate de tener 'datos_clima.csv' actualizado
streamlit run dashboard.py
# Abre en http://<IP_EC2>:8501
```

---

## 🚀 Flujo del Prototipo

1. **EventBridge** programa la invocación de **Lambda** cada cierto tiempo.
2. **Lambda** obtiene los datos de OpenWeather, los transforma y los envía a la API del modelo (EC2 #1).
3. El modelo retorna si hay probabilidad de lluvia.
4. **Lambda** almacena el resultado final en **DynamoDB**.
5. En EC2 #2, el **dashboard de Streamlit** consulta un archivo `.csv` generado a partir de DynamoDB para visualización interactiva.

---

## 📊 Modelo de Predicción

Entrenado usando datos históricos reales (`weatherHistory.csv`) con las siguientes variables:

- Humidity
- Pressure
- Temperature
- Visibility
- Wind Speed

Algoritmo: `RandomForestClassifier` con una precisión estimada superior al 85%.

---

## 📈 Ejemplo de Uso de API (Modelo ML)

**POST** a `/predecir` con JSON:

```json
{
  "humedad": 85,
  "presion": 1012,
  "temperatura": 22,
  "visibilidad": 10,
  "viento": 3,
  "nubes": 90,
  "descripcion": "overcast clouds"
}
```

**Respuesta:**

```json
{
  "lluvia_probable": true,
  "input": {
    "humedad": 85,
    "presion": 1012,
    "temperatura": 22,
    "visibilidad": 10,
    "viento": 3
  }
}
```

---

## 🙋‍♂️ Autores

- **Tomás Suárez**
- **Ricardo Villamizar**
- **Andres Rodriguez**

---

## 📌 Notas Finales

- Este prototipo puede escalarse usando servicios como S3 para ingesta masiva, API Gateway, y servicios de monitoreo avanzado.
- Puedes adaptar el modelo ML para pronósticos más sofisticados con más datos.
