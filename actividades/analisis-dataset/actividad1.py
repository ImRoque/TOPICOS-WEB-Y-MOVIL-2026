from pathlib import Path
import os
import sys
import pandas as pd

BASE = Path(os.getenv("DATASET_DIR", "."))
RUTAS = (BASE, Path("."), Path(__file__).resolve().parents[2])
for p in RUTAS:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from usar_modelo import es_posible


def archivo(nombre):
    for p in RUTAS:
        if (p / nombre).exists():
            return str(p / nombre)
    return nombre


datos = pd.read_csv(archivo("envios_medios.csv"))

print("--- CLIMA VS MEDIO (%) ---")
print((pd.crosstab(datos["clima"], datos["medio_recomendado"], normalize="index") * 100).round(2))

print("\n--- ZONA VS MEDIO (%) ---")
print((pd.crosstab(datos["zona_destino"], datos["medio_recomendado"], normalize="index") * 100).round(2))

print("\n--- LIMITES FISICOS (MIN, MEDIAN, MAX) ---")
print(datos.groupby("medio_recomendado")[["distancia_km", "peso_kg", "volumen_l"]].agg(["min", "median", "max"]))

validos = datos.apply(lambda r: es_posible(r["medio_recomendado"], r), axis=1)
print("\n--- VALIDACION DE REGLAS DEL NEGOCIO (es_posible) ---")
print(f"Envios que cumplen las reglas: {int(validos.sum())} de {len(datos)}")
print(f"Envios que rompen las reglas: {int((~validos).sum())}")

camionetas_cortas = datos[(datos["medio_recomendado"] == "camioneta") & (datos["distancia_km"] < 2)]
justificadas = camionetas_cortas[
    (camionetas_cortas["peso_kg"] > 25)
    | (camionetas_cortas["volumen_l"] > 90)
    | (camionetas_cortas["refrigerado"] == 1)
]
print("\n--- CAMIONETAS EN MENOS DE 2 KM ---")
print(f"Total en < 2 km: {len(camionetas_cortas)}")
print(f"Con razon directa (peso > 25 kg, volumen > 90 L o refrigerado): {len(justificadas)}")
print(f"Restantes (otros factores o ruido): {len(camionetas_cortas) - len(justificadas)}")
