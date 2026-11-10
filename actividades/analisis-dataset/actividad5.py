from pathlib import Path
import os
import sys
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report
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


def entrenar_y_medir(x_tr, y_tr, x_ev, y_ev, class_weight=None):
    prep = ColumnTransformer([
        ("numericas", "passthrough", NUMERICAS),
        ("categoricas", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
    ])
    arbol = DecisionTreeClassifier(
        max_depth=8, min_samples_leaf=5, random_state=42, class_weight=class_weight
    )
    mod = Pipeline([("preparacion", prep), ("arbol", arbol)])
    mod.fit(x_tr, y_tr)
    pred = mod.predict(x_ev)
    acc = accuracy_score(y_ev, pred)
    rep = classification_report(y_ev, pred, output_dict=True, zero_division=0)
    prec_dron = rep["dron"]["precision"]
    rec_dron = rep["dron"]["recall"]
    n_dron_pred = int((pred == "dron").sum())

    df_eval = x_ev.copy()
    df_eval["pred"] = pred
    imposibles = int((~df_eval.apply(lambda r: es_posible(r["pred"], r), axis=1)).sum())
    return len(x_tr), acc, prec_dron, rec_dron, n_dron_pred, imposibles


def imprimir_fila(nombre, metricas):
    n_tr, acc, prec, rec, n_pred, imp = metricas
    print(f"{nombre:<25} | {n_tr:>6} | {acc:.4f} | {prec:.4f} | {rec:.4f} | {n_pred:>4} | {imp:>3}")


print("--- COMPARACION PRINCIPAL (MISMO CONJUNTO DE PRUEBA: 2000 ENVIOS, 190 DRONES REALES) ---")
print("Estrategia                | Entreno| Exact. | Prec.  | Recall | Pred | Imposibles")
imprimir_fila("Sin balancear", entrenar_y_medir(x_entreno, y_entreno, x_prueba, y_prueba, None))
imprimir_fila("Con balanceo (pesos)", entrenar_y_medir(x_entreno, y_entreno, x_prueba, y_prueba, "balanced"))

drones_idx = y_entreno[y_entreno == "dron"].index
x_over = pd.concat([x_entreno, x_entreno.loc[drones_idx], x_entreno.loc[drones_idx], x_entreno.loc[drones_idx]])
y_over = pd.concat([y_entreno, y_entreno.loc[drones_idx], y_entreno.loc[drones_idx], y_entreno.loc[drones_idx]])
imprimir_fila("Oversampling (repetir)", entrenar_y_medir(x_over, y_over, x_prueba, y_prueba, None))

min_clase = len(drones_idx)
indices_sub = []
for clase in sorted(y_entreno.unique()):
    idx_clase = y_entreno[y_entreno == clase].sample(n=min_clase, random_state=42).index
    indices_sub.extend(idx_clase)
imprimir_fila(
    "Submuestreo (recortar)",
    entrenar_y_medir(x_entreno.loc[indices_sub], y_entreno.loc[indices_sub], x_prueba, y_prueba, None),
)

print("\n--- EXPERIMENTO INDEPENDIENTE: HACER TRAMPA (REPETIR DRONES ANTES DE SEPARAR) ---")
drones_total = datos[datos[OBJETIVO] == "dron"]
datos_trampa = pd.concat([datos, drones_total, drones_total, drones_total])
x_t = datos_trampa[NUMERICAS + CATEGORICAS]
y_t = datos_trampa[OBJETIVO]

x_tr_t, x_pr_t, y_tr_t, y_pr_t = train_test_split(
    x_t, y_t, test_size=0.2, stratify=y_t, random_state=42
)

indices_entreno = set(x_tr_t.index)
solapados_total = int(x_pr_t.index.isin(indices_entreno).sum())
es_dron_pr = y_pr_t == "dron"
drones_pr_total = int(es_dron_pr.sum())
drones_solapados = int((es_dron_pr & x_pr_t.index.isin(indices_entreno)).sum())

n_tr_t, acc_t, prec_t, rec_t, pred_t, imp_t = entrenar_y_medir(x_tr_t, y_tr_t, x_pr_t, y_pr_t, None)
print(f"Tamano entreno con trampa: {n_tr_t} | Tamano prueba con trampa: {len(x_pr_t)}")
print(f"Drones en prueba con trampa: {drones_pr_total}")
print(f"Registros de prueba que ya estaban en entreno (solapamiento real): {solapados_total} ({drones_solapados} de {drones_pr_total} drones)")
print(f"Metricas con trampa -> Exactitud: {acc_t:.4f} | Precision dron: {prec_t:.4f} | Recall dron: {rec_t:.4f}")
print(f"Drones predichos en prueba con trampa: {pred_t} | Sugerencias imposibles: {imp_t}")
