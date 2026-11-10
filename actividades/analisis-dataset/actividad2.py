from pathlib import Path
import os
import pandas as pd

BASE = Path(os.getenv("DATASET_DIR", "."))
RUTAS = (BASE, Path("."), Path(__file__).resolve().parents[2])


def archivo(nombre):
    for p in RUTAS:
        if (p / nombre).exists():
            return str(p / nombre)
    return nombre


datos = pd.read_csv(archivo("envios_medios.csv"))

tabla_hora = pd.crosstab(datos["hora_salida"], datos["medio_recomendado"])
print("--- HORA VS MEDIO RECOMENDADO ---")
print(tabla_hora)

noche = (datos["hora_salida"] < 6) | (datos["hora_salida"] >= 21)
print(f"\nEnvios de noche: {noche.sum()} ({noche.mean():.2%})")
print(f"Envios de dia: {(~noche).sum()} ({(~noche).mean():.2%})")

print("\n--- CAMBIO BICICLETAS Y MOTOS EN LA NOCHE ---")
print(tabla_hora.loc[[19, 20, 21, 22], ["bicicleta", "moto"]])
