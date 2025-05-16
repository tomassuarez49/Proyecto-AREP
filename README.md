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

## ⚙️ Instalación y Ejecución

### 🔧 Requisitos previos

Antes de comenzar, asegúrate de tener:

- Una cuenta en AWS con acceso a EC2, Lambda, DynamoDB y EventBridge.
- Dos instancias EC2 (una para el modelo ML y otra para el dashboard).
- Acceso por SSH a ambas máquinas EC2.
- Python 3.9 instalado en ambas instancias (`python3 --version`).
- Claves de API de OpenWeather.

---

### 📦 1. Configurar EC2 para el Modelo ML

1. **Conéctate por SSH** a la primera EC2:

```bash
ssh -i "tu_clave.pem" ec2-user@<IP_EC2_1>
```

2. **Sube los archivos necesarios** (`app.py`, `entrenamiento.py`, `weatherHistory.csv`, `requirements.txt`).

3. **Instala las dependencias**:

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install -r requirements.txt
```

4. **Entrena y guarda el modelo**:

```bash
python3 entrenamiento.py
```

Esto generará `modelo_lluvia.pkl`.

5. **Ejecuta el servidor Flask**:

```bash
python3 app.py
```

Accede al modelo en `http://<IP_EC2_1>:5000/predecir`.

---

### 📦 2. Configurar EC2 para el Dashboard

1. **Conéctate por SSH** a la segunda EC2:

```bash
ssh -i "tu_clave.pem" ec2-user@<IP_EC2_2>
```

2. **Sube los archivos `dashboard.py`, `datos_clima.csv`, `requirements.txt`**.

3. **Instala dependencias**:

```bash
pip3 install -r requirements.txt
```

4. **Ejecuta Streamlit**:

```bash
streamlit run dashboard.py --server.port 8501 --server.enableCORS false
```

5. Accede al dashboard desde tu navegador:

```
http://<IP_EC2_2>:8501
```

⚠️ Asegúrate de que el puerto 8501 esté abierto en el grupo de seguridad de la EC2.

---

### ⚙️ AWS Lambda y EventBridge

1. **Crea una función Lambda** que consuma la API de OpenWeather, llame a la API de predicción y guarde los datos en DynamoDB.
2. Usa **EventBridge** para programar la ejecución automática cada hora o día.
3. Asigna roles IAM con permisos sobre DynamoDB y acceso HTTP.

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

## 📈 Resultados

![image](https://github.com/user-attachments/assets/f6993c47-f46f-4129-9060-43b87c690514)
![image](https://github.com/user-attachments/assets/7211c94f-a7de-47b7-8e99-b9a5ce54f2e0)
![image](https://github.com/user-attachments/assets/f2166c7c-41cd-48c6-a710-7d77b6cbc3c4)



---

## 🙋‍♂️ Autores

- **Tomás Suárez**
- **Ricardo Villamizar**
- **Andres Rodriguez**

---

## 📌 Notas Finales

- Este prototipo puede escalarse usando servicios como S3 para ingesta masiva, API Gateway, y servicios de monitoreo avanzado.
- Puedes adaptar el modelo ML para pronósticos más sofisticados con más datos.
