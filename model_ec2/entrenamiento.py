import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Cargar el dataset
df = pd.read_csv("weatherHistory.csv")

# Eliminar filas sin 'Precip Type'
df = df[df["Precip Type"].notna()]

# Crear columna objetivo binaria: 1 si llueve, 0 si no
df["Lluvia"] = df["Precip Type"].apply(lambda x: 1 if x == "rain" else 0)

# Seleccionar variables predictoras
df = df[["Humidity", "Pressure (millibars)", "Temperature (C)", "Visibility (km)", "Wind Speed (km/h)", "Lluvia"]]

# Eliminar filas con valores faltantes
df.dropna(inplace=True)

# Separar entrada (X) y salida (y)
X = df[["Humidity", "Pressure (millibars)", "Temperature (C)", "Visibility (km)", "Wind Speed (km/h)"]]
y = df["Lluvia"]

# Dividir datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=0)
modelo.fit(X_train, y_train)

# Evaluar
pred = modelo.predict(X_test)
print("Precisión:", accuracy_score(y_test, pred))

# Guardar modelo entrenado
joblib.dump(modelo, "modelo_lluvia.pkl")
print("Modelo guardado como modelo_lluvia.pkl")
