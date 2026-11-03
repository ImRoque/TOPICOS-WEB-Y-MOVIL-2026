# EXAMEN — MICROSERVICIOS, GATEWAY Y EL MONOLITO CON API

**Tópicos Selectos de Tecnologías Web y Móvil**  

**Eduardo Alcaraz**

**Nombre:** Daniel Adrian Roque Cortes  
**Calificación:** __________

---

## 1 — La frase del compañero (10 puntos)

En el pizarrón quedó:

> La API separa clientes del servidor; los microservicios separan servidores entre sí.

Un compañero dice: «Entonces, si mi monolito Django expone una API y además lo meto en Docker, ya cumplí las dos mitades de la frase.»

**a)** Desarmen su argumento. ¿Qué parte de la frase cree cumplir con la API? ¿Qué parte cree cumplir con Docker? ¿En qué se equivoca en cada una?
Con la API cree cumplir la separacion entre el cliente y el servidor porque el frontend se comunica con Django mediante peticiones HTTP, con Docker cree cumplir la separacion entre servidores, pero se equivoca porque Docker solo empaqueta y ejecuta la aplicacion en un contenedor, no separa sus responsabilidades en servicios independientes

**b)** Den un contraejemplo mínimo: mismo código Django, *con* API y *con* Docker, que *sigamos* pudiendo llamar monolito. ¿Qué tendría que añadir (o partir) para que deje de serlo?
Un ejemplo seria un solo proyecto Django con rutas de usuarios, pedidos y recomendar, que tenga su API REST y todo se ejecute dentro del mismo contenedor Docker. Sigue siendo un monolito porque todo pertenece a la misma aplicacion,para dejar de serlo tendria que separar esas responsabilidades en servicios independientes que se puedan ejecutar y desplegar por separado y que se comuniquen mediante una API

**c)** ¿La frase del pizarrón habla de *tecnologías* (Docker, REST) o de *límites de proceso / despliegue*? Defiendan su lectura con lo que vieron en clase.
Habla de los limites de proceso y despliegue porque no importa si utilizamos Docker o REST, lo importante es que cada servicio tenga su propia responsabilidad y pueda funcionar y desplegarse independientemente

---

## 2 — Tres rutas, una trampa (10 puntos)

El equipo muestra este `urls.py` de un solo proyecto Django:

```python
path("usuarios/", ...),
path("pedidos/", ...),
path("recomendar/", ...),
```

y este `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    deploy:
      replicas: 3
```

Afirman: «Tres rutas + tres réplicas = microservicios con alta disponibilidad.»

**a)** Separen las dos ideas que mezclaron (rutas vs réplicas). ¿Qué problema resuelve cada una y cuál *no* resuelve?
Las rutas sirven para organizar las diferentes funcionalidades y permitir que el cliente acceda a cada una mediante una URL, las replicas sirven para tener varias copias de la misma aplicacion y repartir las peticiones, pero ninguna de las dos separa las responsabilidades en microservicios

**b)** Si una de las tres réplicas se cae a mitad de un `POST /pedidos`, ¿el sistema dejó de ser monolito? ¿Por qué sí o por qué no?
No, porque las tres replicas siguen siendo copias de la misma aplicacion Django aunque una se caiga las otras pueden seguir atendiendo peticiones, pero el sistema sigue teniendo la misma estructura de un monolito

**c)** Rediseñen *solo con palabras* el `compose` para que sí ilustre microservicios (nombres de servicios y responsabilidades; no hace falta YAML perfecto). ¿Cuántas *imágenes distintas* mínimo y por qué esa cantidad?
Tendria tres servicios:
- **Gateway:** recibe las peticiones del cliente, valida el acceso y las envia al servicio correspondiente
- **Pedidos:** recibe y guarda los pedidos
- **Recomendar:** utiliza el modelo `.joblib` para recomendar el medio de transporte

Serian tres imagenes distintas porque cada servicio tiene una responsabilidad diferente y necesita poder ejecutarse y desplegarse por separado tambien se podria agregar Notificar como otro servicio para enviar correos sin afectar la creacion de pedidos

---

## 3 — El gateway que «hace de más» (10 puntos)

Les proponen este diseño «para no complicar»:

> Un solo contenedor nginx+Python que: valida el JWT, elige el medio con el `.joblib`, guarda el pedido en SQLite, manda el correo y devuelve el HTML.

Lo llaman «API Gateway».

**a)** ¿Es un gateway? Si no, ¿qué es? Usen la analogía del recepcionista (o otra) y digan qué oficios mezclaron.
No es un Gateway porque esta haciendo muchas cosas que no le corresponden. Un Gateway seria como un recepcionista que recibe al cliente, valida su acceso y lo dirige al area correspondiente, en este caso tambien esta recomendando el transporte, guardando pedidos, enviando correos y mostrando HTML, mezclando varias responsabilidades en un solo lugar

**b)** Mencionen *tres* consecuencias malas de ese diseño cuando el modelo pesado se reentrena cada semana y el correo empieza a fallar.
1. Cada vez que se actualice el modelo podria ser necesario reiniciar todo el contenedor y afectar las demas funciones
2. Si el correo falla podria provocar que falle toda la peticion aunque el pedido ya se haya guardado
3. No se pueden escalar las partes por separado y el modelo pesado podria consumir recursos que necesita la creacion de pedidos

**c)** Partan ese contenedor en piezas. Para cada pieza digan: ¿queda en el borde (gateway) o detrás? No inventen diez servicios: el mínimo que separe borde, logística e (si hace falta) aviso.
Lo separaria de la siguiente manera:
- **Gateway (borde):** valida el JWT y dirige las peticiones a los servicios
- **Pedidos (detras):** guarda los pedidos y se encarga de la logistica
- **Recomendar (detras):** carga el modelo `.joblib` y recomienda el medio de transporte
- **Notificar (detras, opcional):** se encarga de enviar los correos cuando se crea un pedido

Asi cada parte tiene una responsabilidad y si el correo falla no tiene porque detener la creacion del pedido

---

## 4 — `localhost`, la trampa favorita (10 puntos)

Pedidos corre en un contenedor. Recomendar en otro, misma Compose. Alguien «arregla» la conexión así:

```text
RECOMENDAR_URL=http://127.0.0.1:8002
```

En su laptop, *sin* Docker, ese `curl` a `127.0.0.1:8002` sí funcionaba.

**a)** Expliquen por qué en Compose ese arreglo suele fallar *aunque* Recomendar esté sano. ¿A qué proceso apunta `127.0.0.1` desde dentro de Pedidos?
Porque dentro de Docker cada contenedor tiene su propia direccion y localhost apunta al mismo contenedor donde se esta ejecutando entonces desde Pedidos estaria buscando el servicio Recomendar dentro de su propio contenedor y no lo encontraria

**b)** ¿Por qué `http://recomendar:8002` sí tiene chance de funcionar? ¿Quién «inventa» el nombre `recomendar`?
Porque Docker Compose crea una red entre los contenedores y permite que se comuniquen utilizando el nombre de sus servicios,el nombre recomendar lo establece Docker Compose cuando se define el servicio en el archivo `docker-compose.yml`

**c)** Ahora Recomendar se muda a la laptop de otro alumno (`192.168.0.57`). Escriban la URL que pondrían *y* dos cosas que tienen que ser verdad en la WiFi para que no sea teatro (puertos, firewall, etc.). Si solo cambian la URL y nada más, ¿qué puede seguir fallando?
La URL seria `http://192.168.0.57:8002`. Para que funcione las dos laptops deben poder comunicarse por la misma red y el puerto 8002 debe estar permitido por el firewall tambien el servicio debe estar configurado para recibir conexiones externas y no solamente desde localhost, si solo cambiamos la URL podria seguir fallando porque el firewall puede bloquear la conexion o la WiFi puede impedir que los dispositivos se comuniquen entre si

---

## 5 — Fallo parcial con números (10 puntos)

Escenario medido en laboratorio (inventado pero coherente):

- 1000 `POST /pedidos` por hora en promedio
- Recomendar tarda 200 ms cuando está bien
- El 5 % del tiempo Recomendar no responde (timeout 3 s)
- Pedidos, si hay timeout, usa plan B (moto) y responde 200 en 50 ms
- El gateway añade 5 ms

**a)** En la hora «normal» (Recomendar bien), ¿el cliente espera ~200 ms o ~3 s? ¿Quién pone el tiempo dominante?
El cliente espera aproximadamente 200 ms porque Recomendar es quien tarda mas en responder y es el que pone el tiempo dominante, sumando los 50 ms de Pedidos y los 5 ms del Gateway serian aproximadamente 255 ms en total

**b)** En el 5 % malo, con plan B: ¿el cliente ve error o pedido creado? ¿Qué «mentira útil» están aceptando (medio quizá no óptimo)?
El cliente ve un pedido creado con respuesta 200 porque Pedidos utiliza el plan B y asigna una motocicleta. La mentira util es que se esta aceptando un medio que posiblemente no sea el mas conveniente, pero permite que el pedido se registre aunque Recomendar no este disponible, en este caso el cliente podria esperar aproximadamente 3 segundos por el timeout antes de recibir la respuesta

**c)** Un compañero dice: «Mejor que Pedidos *reintente* 10 veces hasta que Recomendar vuelva; así nunca usamos plan B.» ¿Qué le pasa a la cola de peticiones y al gateway si Recomendar está caído 10 minutos? ¿Plan B siempre es peor que reintentar? Argumenten.
La cola de peticiones comenzaria a crecer porque cada pedido estaria esperando a que Recomendar responda y si cada intento tarda 3 segundos podria llegar a esperar hasta 30 segundos. Esto tambien afectaria al Gateway porque tendria muchas peticiones esperando y podria dejar de responder correctamente

El plan B no siempre es peor porque permite continuar con el proceso cuando Recomendar falla, mientras que reintentar puede provocar mas retrasos, depende de que tan importante sea obtener la recomendacion exacta para poder crear el pedido

---

## 6 — Apagan el «edificio equivocado» (10 puntos)

Tres contenedores: gateway, pedidos, recomendar. Hacen tres experimentos *por separado*:

1. `docker compose stop gateway`
2. `docker compose stop pedidos`
3. `docker compose stop recomendar`

Para *cada* experimento digan qué ve el navegador en `http://IP:8080/` (página / crear pedido) y qué sigue vivo por dentro. No basta «no jala»: digan *qué* no jala y qué sí podría seguir respondiendo si alguien hablara por dentro de la red.

Luego: ¿en cuál de los tres el sistema «parece» más muerto hacia afuera aunque más piezas sigan arriba? ¿Qué les enseña eso del borde?

1. **Si apagamos Gateway:** El navegador no podria acceder a la pagina ni crear pedidos porque el Gateway es la unica entrada desde el exterior. Sin embargo, Pedidos y Recomendar seguirian funcionando por dentro y podrian comunicarse entre ellos

2. **Si apagamos Pedidos:** El navegador podria seguir mostrando la pagina si esta servida por Gateway, pero no podria crear pedidos porque ese servicio ya no estaria disponible. Recomendar seguiria funcionando y podria responder directamente si alguien lo consulta por dentro

3. **Si apagamos Recomendar:** El navegador podria seguir mostrando la pagina y Pedidos seguiria funcionando. Al crear un pedido, Pedidos intentaria comunicarse con Recomendar, pero al no encontrarlo utilizaria el plan B si esta configurado, de lo contrario devolveria un error

**Luego:**
Cuando apagamos el Gateway porque aunque Pedidos y Recomendar sigan funcionando por dentro, el cliente ya no tiene una entrada para comunicarse con ellos. Esto demuestra que el Gateway es una parte muy importante porque centraliza la entrada al sistema, pero tambien puede convertirse en un punto unico de falla

---

## 7 — WiFi del salón, conflicto de roles (10 puntos)

Cuatro alumnos:

- Ana: gateway + HTML
- Beto: pedidos
- Carla: recomendar
- Diana: «yo también levanté un gateway en mi laptop por si Ana falla»

Todos en la misma WiFi. El cliente (otro equipo) configura a veces la IP de Ana y a veces la de Diana.

**a)** ¿Qué problema de *diseño* introdujo Diana aunque «todo responda 200»? (Piensen en una sola puerta vs dos puertas.)
Diana introdujo una segunda puerta de entrada al sistema y eso puede provocar que los clientes lleguen a diferentes Gateway. El problema es que podrian tener configuraciones o versiones diferentes y no se estaria utilizando una sola entrada para controlar las peticiones. Para que exista alta disponibilidad no basta con levantar otro Gateway, tambien se necesita una forma de dirigir las peticiones correctamente

**b)** Beto configuró `RECOMENDAR_URL=http://localhost:8002` porque en su máquina desarrolló Pedidos y Recomendar juntos. En el salón Recomendar está en la laptop de Carla. ¿Qué falla y cómo lo corrigen *sin* juntar otra vez los dos servicios en la laptop de Beto?
Falla porque localhost apunta a la laptop o contenedor de Beto y no a la computadora de Carla donde se encuentra Recomendar. Lo corregiria colocando la IP de Carla y el puerto donde esta funcionando Recomendar, por ejemplo `http://IP_DE_CARLA:8002`, asegurando que el firewall permita la conexion y que ambas computadoras puedan comunicarse por la WiFi

**c)** La WiFi del campus aísla clientes («AP isolation»). `ping` entre alumnos falla. ¿Pueden hacer la práctica tal cual? Si no, propongan *un* plan B de laboratorio que preserve la lección «procesos separados» (aunque no sea WiFi del salón).
No se puede realizar tal cual porque aunque todos esten conectados a la misma WiFi no pueden comunicarse directamente entre ellos. Como plan B utilizaria una sola laptop con Docker Compose donde se ejecuten los tres contenedores por separado. Asi se mantiene la comunicacion entre procesos independientes sin depender de la WiFi del salon

---

## 8 — El front que conoce demasiado (10 puntos)

El HTML hace esto al enviar el formulario:

```javascript
await fetch("http://192.168.1.20:8002/sugerir", { ... }); // Recomendar
await fetch("http://192.168.1.30:8001/pedidos", { ... }); // Pedidos
```

El autor dice: «Más rápido: me salto el gateway.»

**a)** Listen *tres* problemas (seguridad, cambio de IP, orden de llamadas, consistencia del folio, CORS, etc.).
1. El frontend conoce las direcciones internas de los servicios y eso puede representar un problema de seguridad
2. Si cambia la IP de algun servicio se tendria que modificar el frontend para que pueda seguir funcionando
3. Se pueden generar problemas si Recomendar responde correctamente pero Pedidos falla, porque ya se hizo una llamada pero no se completo la creacion del pedido

**b)** Rediseñen la secuencia correcta con gateway: *una* llamada desde el navegador. ¿Quién habla con Recomendar y por qué no el navegador?
El navegador solamente enviaria una peticion al Gateway y este la enviaria a Pedidos. Despues Pedidos se comunicaria con Recomendar para obtener el medio de transporte y finalmente guardaria el pedido y devolveria el folio
Pedidos debe hablar con Recomendar porque es quien se encarga de crear el pedido y necesita esa informacion para completar el proceso. Asi el navegador no necesita conocer las direcciones internas de los servicios

**c)** El selector de modelo (`arbol=|=bosque=|=red') va en el JSON. Si el front llama directo a Recomendar *y* a Pedidos, ¿quién debería crear el folio para no duplicar lógica? ¿Qué invariante rompen si los dos «crean» algo?
Pedidos debe crear el folio porque es el encargado de registrar y guardar los pedidos. Si Recomendar y Pedidos crean sus propios folios se podria duplicar la informacion y terminar con identificadores diferentes para una misma solicitud. Por eso debe existir un solo servicio encargado de crear y controlar el folio

---

## 9 — El LLM vendedor (10 puntos)

Producto: tienda + envíos.

- Modelo `.joblib`: medio de transporte
- LLM: texto para convencer al cliente en la ficha del producto

Un arquitecto propone *un solo* microservicio `cerebro` que: recibe el carrito, elige el medio con el árbol *y* genera el pitch de ventas con el LLM, todo en la misma petición `/inteligente`.

**a)** Critiquen el nombre y el corte. ¿Qué dos oficios distintos mezclaron? ¿Qué falla cuando el LLM tarda 8 s y el despacho necesita responder en < 500 ms?
El nombre cerebro no explica realmente que responsabilidad tiene el servicio y esta mezclando dos funciones diferentes, la recomendacion del medio de transporte y la generacion de textos para ventas. Si el LLM tarda 8 segundos retrasaria todo el proceso de despacho aunque esa parte no necesite utilizarlo

**b)** Propongan dos endpoints (o dos servicios) y digan cuál usa el *front de tienda* y cuál el *flujo de pedido/envío*.
Separaria los servicios de esta manera:

- `POST /productos/pitch`: genera los textos para convencer al cliente y lo utilizaria el front de la tienda
- `POST /recomendar/medio`: utiliza el modelo `.joblib` para recomendar el medio de transporte y lo utilizaria Pedidos durante el proceso de envio

Asi cada servicio tiene una responsabilidad diferente y no se afectan entre si

**c)** El LLM vive en un server con GPU en otra red. El front de tienda ¿apunta a la GPU o al gateway? Si mañana cambian de proveedor LLM (otro host), ¿qué archivo/config quieren tocar *una sola vez*?
El front de la tienda debe apuntar al Gateway porque es la unica entrada al sistema y no deberia conocer las direcciones internas de los servicios. Si se cambia el proveedor del LLM solo modificaria la URL del nuevo servidor en la configuracion del servicio que lo utiliza, por ejemplo en una variable de entorno `LLM_URL`, sin tener que modificar el frontend

---

## 10 — El inversionista y la semana imposible (10 puntos)

Hoy:

- Panel interno: monolito Django (funciona, poco tráfico)
- App clientes: gateway + pedidos + recomendar
- Idea: LLM de ventas (aún no)
- Equipo: 5 personas
- Inversionista: «Todo a microservicios en 7 días, incluido el panel, o no hay dinero»

**a)** Escriban la respuesta al inversionista (máx. 8 líneas) con postura *y* riesgo concreto si obedecen a ciegas.
No recomendaria cambiar todo a microservicios en solo 7 dias porque el panel actualmente funciona y tiene poco trafico. Primero revisaria que partes realmente necesitan separarse y cuales pueden seguir funcionando como estan. Hacerlo todo de golpe puede provocar errores, problemas de comunicacion y fallas en el sistema. Ademas el equipo tendria que dedicar tiempo a mantener varios servicios en lugar de mejorar las funcionalidades que realmente se necesitan

**b)** Ordenen *estas cuatro* iniciativas de más a menos urgente para *esta* semana y justifiquen el orden (no el catálogo soñado):
1. Partir el panel Django en 6 microservicios
2. Sacar el reentrenamiento del `.joblib` a un pipeline que no tumbe Pedidos
3. Meter auth + rate limit en el gateway público
4. Subir el LLM de ventas a producción sin timeouts ni plan B
1. **Opcion 3:** Meter auth + rate limit en el Gateway publico porque es importante proteger el acceso al sistema y evitar peticiones no permitidas o excesivas

2. **Opcion 2:** Separar el reentrenamiento del `.joblib` porque no deberia afectar el funcionamiento de Pedidos cada vez que se actualice el modelo

3. **Opcion 4:** No lo subiria a produccion todavia porque si el LLM tarda demasiado o deja de responder podria afectar todo el proceso. Primero agregaria timeouts y un plan B

4. **Opcion 1:** No dividiria el panel Django en este momento porque funciona correctamente y tiene poco trafico, por lo que no es una necesidad urgente

**c)** Inventen *una* métrica que les diga «ya toca partir X del monolito» (no «porque está de moda»). Tiene que ser observable (tiempo, errores, despliegues, equipo…).
Una metrica seria la cantidad de veces que una modificacion de un modulo obliga a reiniciar todo el monolito durante el mes. Si esto ocurre constantemente y provoca tiempo fuera de servicio, seria una señal de que ese modulo podria separarse para poder actualizarlo sin afectar las demas partes

**d)** Cierren con una frase propia (no copien el apunte) que capture: ¿microservicios son el objetivo o la herramienta?
Los microservicios no son el objetivo, son una herramienta para separar responsabilidades cuando el crecimiento del sistema realmente lo necesita

