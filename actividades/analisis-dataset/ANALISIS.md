## Actividad 1 — El retrato del dataset

### 1. Prediccion
- Cuando llueva creo que va a dominar la camioneta, mas que nada porque tapa los paquetes del agua y el repartidor no se moja tanto
- En el centro de la ciudad creo que va a dominar la bici, porque hay mucho trafico para los carros y las distancias son cortas
- Para la distancia maxima de la bici calculo entre 5 y 8 km, que es lo normal para moverse pedaleando en la ciudad
- Sobre si van a salir filas que rompan reglas, creo que si van a salir algunas porque siempre se cuela ruido o errores en los datos

### 2. Comprobacion
- Con lluvia domino la moto con 74.83%, la camioneta saco 16.68%, la bici 8.49% y el dron 0%
- En el centro gano la bici con 58.45%, luego quedo la moto con 28.03% y la camioneta con 13.52%, mientras que el dron saco 0%
- En los maximos la bici llego a 7.00 km, la moto a 39.90 km, el dron a 14.99 km y la camioneta hasta 59.12 km
- Para las filas que rompen las reglas no saque el conteo exacto al aplicar es_posible por lo que no pongo una cantidad exacta, para checar esto bien toca revisar cada etiqueta del CSV contra las reglas y no nomas asumir que el ruido hace cosas imposibles

### 3. Decision (Preguntas)
1. El dron nunca sale en el centro ni en zona rural, en el centro no vuela por ser espacio aereo restringido y a la zona rural no llega porque se pasa de su limite de 15 km, tampoco sale con lluvia o viento porque las reglas solo lo dejan volar con clima despejado
2. La columna que dice por que la bici casi no va a la periferia es distancia_km, casi todos esos viajes superan su tope de 7 km, ahi se ve claro que la distancia es la principal traba para usar la bici
3. Comparando los maximos con la tabla de limites se ven clarito los topes de distancia de la bici (7 km), moto (40 km) y dron (15 km), pero el maximo de la camioneta no es una regla del negocio sino nada mas el paquete mas grande que salio en el dataset
4. Salieron 107 camionetas en viajes cortos de menos de 2 km, casi todas se justifican porque llevan mas de 25 kg, pasan de 90 L o llevan producto refrigerado, las que no cumplen eso seguro son por lluvia, paquetes fragiles o puro ruido del generador, pero no saque el numero exacto de cuantas son de cada una
- Para pensar: viendo puro CSV si se pueden reconocer algunos limites porque se repiten mucho como las distancias maximas, pero no todas las reglas se pueden sacar asi, sobre todo las de clima o zonas, dejar que el modelo aprenda todo solo es peligroso porque podria mandar un dron lloviendo si no hay regla que lo pare

---

## Actividad 2 — La hora y el dron

### 1. Prediccion
- A las 3:00 am creo que van a salir 0 drones porque tienen prohibido volar de noche
- De envios de noche le calculo entre un 10% y 15% porque casi todos los pedidos caen de dia

### 2. Comprobacion
- A las 3:00 salieron exactamente 0 pedidos en dron
- Los envios de noche (antes de las 6 o despues de las 21) fueron 1053 que son el 10.53%, mientras que de dia hubo 8947 envios
- Comparando con lo que creia si le atine porque el porcentaje cayo justo en el rango que esperaba con 10.53%

### 3. Decision (Preguntas)
1. Entre las 21:00 y las 5:00 no hay ni un viaje en dron, lo que cuadra perfecto con la regla que prohibe vuelos de noche en ese horario
2. Hay 1053 envios de noche contra 8947 de dia, como el modelo ve muy poquitos ejemplos de noche no tiene tanta info para aprender bien que hacer a esas horas
3. Entre las 20:00 y las 21:00 las bicis caen de 115 a 20 y las motos suben de 160 a 240, esto pasa porque el sistema le baja puntos a la bici en la noche para cuidar al repartidor
4. El arbol solo hace preguntas de si una variable es menor o igual a algo, por eso a fuerzas necesita minimo dos preguntas para aislar la noche porque las horas nocturnas quedan partidas en los dos extremos del reloj (de 0 a 5 y de 21 a 23)
- Para pensar: haria una columna que se llame es_noche que valga 1 si la hora es menor a 6 o mayor o igual a 21 y 0 para el resto, para ver si jalo entrenaria de nuevo el modelo y checaria si esa columna agarra importancia y ayuda a bajar los fallos nocturnos

---

## Actividad 3 — Anatomia de los errores

### 1. Prediccion
- Para mi la confusion mas comun va a ser entre moto y bici porque se cruzan en paquetes chicos y viajes cortos
- No creo que el modelo confunda una bici con una camioneta porque la diferencia en peso y tamaño de los paquetes es muchisima

### 2. Comprobacion
- El modelo tuvo 158 errores en los datos de prueba, lo que mas se confundio fue moto mandada a bici con 46 casos, luego camioneta a moto con 32 y moto a dron con 29
- El modelo jamas cruzo una bici con una camioneta, salieron 0 casos de esos
- Comparando con mi prediccion le atine a que el fallo principal seria entre moto y bici y tambien a que no cruzaria bicis con camionetas

### 3. Decision (Preguntas)
1. Hubo 158 errores y casi todos pasan entre transportes muy parecidos en capacidad y distancia, lo que demuestra que al modelo le cuesta distinguir cuando el pedido queda justo en el limite de dos opciones
2. De las 29 motos que el modelo mando a dron hay 26 que eran de noche, ahi las reglas del negocio las descartan solas porque el dron no vuela a esa hora, los 3 casos que quedan fueron de dia con paquetes ligeros que cabian en dron pero la moto salia mas barata
3. Las 46 motos que el modelo mando a bici son viajes de menos de 7 km con tope de 6.89 km, la cosa es que algunas llevaban pesos mas altos de lo que aguanta la bici o iban con lluvia, ahi se ve que la pura distancia no alcanza para separar bien los casos
- Para pensar: yo arreglaria primero el error de mandar motos a dron porque mandar un dron a lo tonto sale muy caro y es peligroso, por eso mejor dejo que las reglas del negocio bloqueen lo que no se puede en lugar de depender nomas de lo que diga el modelo

---

## Actividad 4 — Que columnas usa de verdad el modelo?

### 1. Prediccion
Antes de ver las importancias mi orden de mayor a menor es este:
1. distancia_km
2. peso_kg
3. volumen_l
4. refrigerado
5. clima
6. hora_salida
7. fragil
8. prioridad
9. largo_cm
10. ancho_cm
11. alto_cm
12. valor_declarado_mxn
13. zona_destino
14. trafico

Siento que distancia_km, peso_kg y volumen_l van a tener mas peso porque son los limites fisicos de cada vehiculo, y zona_destino o trafico seguro casi no importan para el arbol aunque la app los siga pidiendo para otras cosas

### 2. Comprobacion
- Las columnas con mas importancia fueron distancia_km con 0.322, volumen_l con 0.193, clima con 0.144, refrigerado con 0.131 y peso_kg con 0.126
- La exactitud del modelo original era de 0.921, al quitar distancia_km cayo a 0.793 que es una bajada de 0.128
- Al quitar zona_destino la exactitud se quedo igualita en 0.921, y quitar trafico tampoco le movio nada al resultado

### 3. Decision (Preguntas)
1. Las que mas destacaron fueron distancia_km, volumen_l, clima y refrigerado, cuadra casi todo con mi prediccion aunque no esperaba que el clima pesara tanto
2. La variable que mas tira la exactitud al quitarla es distancia_km bajando 0.128, mientras que zona_destino y trafico no cambian para nada el resultado
3. Que zona_destino tenga importancia cero para el arbol no significa que no sirva, el modelo aprende de los datos pero las reglas del negocio se aplican despues para bloquear cosas como volar un dron al centro
- Para pensar: la aplicacion tiene que seguir pidiendo la zona de destino aunque el arbol ni la pele, ese dato sirve para aplicar las reglas, armar las rutas y calcular cuanto cobrar por el viaje

---

## Actividad 5 — El dron es minoria: hay que balancear el dataset?

### Parte A — Pensar antes de tocar los datos
1. Un modelo que nunca mande dron y le atine a todo lo demas tendria 90.5% de exactitud, y uno que tire pura moto tendria 45.8%, esto demuestra que la exactitud engaña feo cuando las clases estan disparejas, por eso conviene mas checar precision y recall del dron
2. Hay poquitos drones porque el negocio tiene un buen de restricciones para usarlos y no llegan a todos lados, asi que no es error de los datos sino que asi es la operacion real
3. Si se va a balancear tiene que ser despues de separar los datos y nada mas en los de entrenamiento, los de prueba se dejan intactos con su proporcion original para ver como responde el modelo con envios reales

### Parte B — Probar estrategias
Para comparar use los mismos 2,000 envios de prueba donde vienen 190 drones reales, probe dos estrategias (class_weight y oversampling) ademas de la linea base y no puse numeros de submuestreo porque no lo corri y no queria inventar datos:

| Estrategia | Envios entrenamiento | Exactitud | Precision dron | Recall dron | Veces predice dron (reales: 190) | Sugerencias imposibles |
|---|---:|---:|---:|---:|---:|---:|
| Sin balancear | 8000 | 0.92 | 0.84 | 0.91 | 205 | 31 |
| Con balanceo (class_weight) | 8000 | 0.90 | 0.77 | 1.00 | 248 | 35 |
| Oversampling (repetir drones) | 10274 | 0.90 | 0.72 | 1.00 | 263 | 56 |

Ahi se ve que class_weight y oversampling suben el recall a 1.00 pero le dan en la torre a la precision y avientan mas sugerencias imposibles, encontrar todos los drones no significa que todo lo que recomiende este bien

**Experimento haciendo trampa antes de separar los datos**
Hice una prueba repitiendo datos del dron antes de separar entrenamiento y prueba, esto hace que los mismos registros caigan en ambos lados y el modelo se evalue con cosas que ya memorizo.
Con este experimento saque una exactitud de 0.925 y precision de dron de 0.97, pero esa mejora es pura mentira porque la separacion ya no es independiente cuando hay filas repetidas.

### Parte C — Interpretar
1. Usando class_weight el recall de dron subio de 0.91 a 1.00 pero la precision se cayo de 0.84 a 0.77, el modelo encuentra mas drones reales pero se equivoca mas recomendando cosas que no son
2. El submuestreo recorta un buen de datos de las clases mayores para emparejar todo, se achica el entrenamiento y se pierde informacion valiosisima de motos, bicis y camionetas
3. class_weight y oversampling dan numeros parecidos porque en el fondo buscan lo mismo que es darle mas peso a la clase minoritaria, uno castiga mas los errores y el otro repite filas pero terminan haciendo casi lo mismo
4. Despues de balancear ya no te puedes fiar del porcentaje de confianza igual que antes, porque el modelo se entreno con una distribucion inflada que no refleja la demanda real de todos los dias

### Parte D — Decidir
- Para pensar: por ahora prefiero dejar el modelo sin balancear y apoyarme en la funcion es_posible para bloquear lo que rompa las reglas, mandar un dron a lo tonto sale mas caro que mandar una moto, y aunque el balanceo mejora el recall tambien dispara las cosas imposibles, si despues compran mas drones los datos reales subiran solos y ahi si convendra reentrenar con proporciones verdaderas