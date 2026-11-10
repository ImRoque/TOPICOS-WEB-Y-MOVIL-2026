from pathlib import Path
import os
import sys
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

BASE = Path(os.getenv("DATASET_DIR", "."))
RUTAS = (BASE, Path("."), Path(__file__).resolve().parents[2])
for p in RUTAS:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from entrenar_arbol import NUMERICAS, CATEGORICAS, OBJETIVO


def archivo(nombre):
    for p in RUTAS:
        if (p / nombre).exists():
            return str(p / nombre)
    return nombre


datos = pd.read_csv(archivo("envios_medios.csv"))
columnas_originales = NUMERICAS + CATEGORICAS
x = datos[columnas_originales]
y = datos[OBJETIVO]

x_entreno, x_prueba, y_entreno, y_prueba = train_test_split(
    x, y, test_size=0.2, stratify=y, random_state=42
)

modelo = joblib.load(archivo("modelo_medios.joblib"))
nombres_oh = list(modelo.named_steps["preparacion"].get_feature_names_out())
importancias_oh = modelo.named_steps["arbol"].feature_importances_

imp_por_columna = {col: 0.0 for col in columnas_originales}
for nombre, valor in zip(nombres_oh, importancias_oh):
    limpio = nombre.split("__", 1)[1]
    for col in columnas_originales:
        if limpio == col or limpio.startswith(col + "_"):
            imp_por_columna[col] += float(valor)
            break

df_imp = (
    pd.DataFrame({
        "columna": list(imp_por_columna.keys()),
        "importancia": list(imp_por_columna.values()),
    })
    .sort_values("importancia", ascending=False)
    .reset_index(drop=True)
)
df_imp.index = df_imp.index + 1
print(f"--- IMPORTANCIA AGRUPADA DE LAS {len(df_imp)} COLUMNAS ORIGINALES ---")
print(df_imp.round(4))

base_acc = (modelo.predict(x_prueba) == y_prueba).mean()
print(f"\nExactitud original con las 14 columnas: {base_acc:.4f}")
print("\n--- IMPACTO EN EXACTITUD AL QUITAR CADA UNA DE LAS 14 COLUMNAS ---")

resultados_quitar = []
for col in columnas_originales:
    num = [c for c in NUMERICAS if c != col]
    cat = [c for c in CATEGORICAS if c != col]
    prep = ColumnTransformer([
        ("numericas", "passthrough", num),
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), cat),
    ])
    mod = Pipeline([
        ("preparacion", prep),
        ("arbol", DecisionTreeClassifier(max_depth=8, min_samples_leaf=5, random_state=42)),
    ])
    mod.fit(x_entreno[num + cat], y_entreno)
    acc = (mod.predict(x_prueba[num + cat]) == y_prueba).mean()
    resultados_quitar.append({
        "columna_eliminada": col,
        "exactitud_sin_columna": round(acc, 4),
        "cambio": round(acc - base_acc, 4),
    })

df_quitar = pd.DataFrame(resultados_quitar).sort_values("cambio")
print(df_quitar.to_string(index=False))
