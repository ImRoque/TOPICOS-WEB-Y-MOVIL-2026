from pathlib import Path
import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

BASE = Path(os.getenv("DATASET_DIR", "."))
RUTAS = (BASE, Path("."), Path(__file__).resolve().parents[2])
for p in RUTAS:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from entrenar_arbol import NUMERICAS, CATEGORICAS, OBJETIVO
from usar_modelo import es_posible


def archivo(nombre):
    for p in RUTAS:
        if (p / nombre).exists():
            return str(p / nombre)
    return nombre


datos = pd.read_csv(archivo("envios_medios.csv"))
x = datos[NUMERICAS + CATEGORICAS]
y = datos[OBJETIVO]

x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=42
)

modelo = joblib.load(archivo("modelo_medios.joblib"))
prediccion = modelo.predict(x_prueba)

tabla = x_prueba.copy()
tabla["real"] = y_prueba
tabla["predicho"] = prediccion

errores = tabla[tabla["real"] != tabla["predicho"]]
print(f"Total de errores en prueba: {len(errores)} de {len(x_prueba)}")

print("\n--- CONFUSIONES MAS FRECUENTES ---")
print(errores.groupby(["real", "predicho"]).size().sort_values(ascending=False))

moto_dron = errores[(errores["real"] == "moto") & (errores["predicho"] == "dron")]
es_noche = (moto_dron["hora_salida"] < 6) | (moto_dron["hora_salida"] >= 21)
corregidos = ~moto_dron.apply(lambda r: es_posible("dron", r), axis=1)
no_corregidos = moto_dron[~corregidos]

print("\n--- ANALISIS: MOTO ENVIADA A DRON ---")
print(f"Total moto -> dron: {len(moto_dron)}")
print(f"De noche (< 6 o >= 21): {int(es_noche.sum())}")
print(f"Descartados por reglas (es_posible): {int(corregidos.sum())}")
print(f"No descartados por reglas: {len(no_corregidos)}")
if len(no_corregidos) > 0:
    print("Resumen de los casos no descartados (min, median, max):")
    print(no_corregidos[["distancia_km", "peso_kg", "volumen_l", "hora_salida"]].agg(["min", "median", "max"]).round(2))
    print("Clima / Zona / Prioridad en no descartados:", no_corregidos[["clima", "zona_destino", "prioridad"]].value_counts().to_dict())

moto_bici = errores[(errores["real"] == "moto") & (errores["predicho"] == "bicicleta")]
bici_ok = tabla[(tabla["real"] == "bicicleta") & (tabla["predicho"] == "bicicleta")]


def resumir_grupo(df):
    noche_g = (df["hora_salida"] < 6) | (df["hora_salida"] >= 21)
    return pd.Series({
        "casos": len(df),
        "dist_mediana_km": round(df["distancia_km"].median(), 2),
        "dist_max_km": round(df["distancia_km"].max(), 2),
        "peso_mediano_kg": round(df["peso_kg"].median(), 2),
        "peso_max_kg": round(df["peso_kg"].max(), 2),
        "vol_mediano_l": round(df["volumen_l"].median(), 2),
        "con_lluvia_%": round((df["clima"] == "lluvia").mean() * 100, 1),
        "de_noche_%": round(noche_g.mean() * 100, 1),
        "fragil_%": round((df["fragil"] == 1).mean() * 100, 1),
    })


print("\n--- COMPARATIVA: MOTO->BICICLETA VS BICICLETAS BIEN CLASIFICADAS ---")
comparativa = pd.DataFrame({
    "moto_a_bici": resumir_grupo(moto_bici),
    "bici_acertada": resumir_grupo(bici_ok),
})
print(comparativa)
