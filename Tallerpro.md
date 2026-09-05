# TallerPro

## Contexto encontrado

TallerPro es una aplicación para administrar un taller mecánico, aunque `SISTEMA.txt` continúa describiendo una clínica dental. La situación resulta especialmente contradictoria porque la documentación prohíbe el patrón Chain of Responsibility y el proyecto sí contiene una implementación de dicho patrón.

## Revisión técnica

### Autenticación y autorización

`Handler.js` contiene `Handler`, `AuthHandler` y `BitacoraHandler`, pero la cadena solo participa en una de las rutas. En otras partes de `app.js` se repiten comprobaciones de sesión y cookies.

La situación más grave es `admin_bypass`: una cookie puede provocar que el servidor asuma privilegios de jefe sin comprobar su autenticidad.

Además, `/entrega` y `/inventario` presentan problemas de protección. La primera modifica datos mediante GET y la segunda expone información del inventario sin exigir sesión.

**Solución:** establecer un único mecanismo de autorización para las rutas protegidas, eliminar la cookie administrativa y hacer que las operaciones que modifican datos utilicen POST con autenticación.

### Consultas SQL

El login construye la consulta concatenando correo y contraseña. El mismo patrón aparece al procesar órdenes, inventario y entrega.

Esto permite inyección SQL y, en el caso de las contraseñas, se combina con almacenamiento en texto plano.

**Solución:** utilizar placeholders de `mysql2` en todas las consultas y `bcrypt` para almacenar y verificar contraseñas.

### Proceso de cobro

`CobroOrden` mezcla el cálculo del costo, el cobro bancario y las actualizaciones de la orden. El XML se construye manualmente y la respuesta bancaria se valida mediante una búsqueda de texto.

Después del cobro se realizan varias escrituras relacionadas sin una transacción. Un fallo entre ellas puede dejar una orden creada parcialmente o un mecánico en un estado incorrecto.

**Solución:** separar la lógica de negocio y envolver las escrituras en una transacción con `beginTransaction`, `commit` y `rollback`. El pago debe utilizar una integración segura y una validación criptográfica.

### Peticiones y correo

La aplicación realiza peticiones HTTP locales en bucle para construir información de la página principal. También consulta cada refacción de forma individual, generando N+1.

El sistema de correo utiliza `jsonTransport`, por lo que el mensaje no se envía mediante SMTP: solamente se serializa internamente.

**Solución:** reducir las consultas mediante JOIN, mejorar las llamadas HTTP y configurar un transporte de correo real.

### Otros elementos

El parseo de cookies está implementado manualmente, aunque existe una solución estándar como `cookie-parser`. `app.old.js` es una copia antigua que no aporta funcionalidad y debe considerarse código muerto.

El secreto de `express-session` es `password`, está escrito directamente en el código y es fácilmente predecible. También existe el CSS de 90 clases repetitivas y no hay pruebas automatizadas.

## Orden de trabajo sugerido

**Seguridad:** autenticación, `admin_bypass`, SQL y contraseñas.

**Integridad:** transacciones del cobro y protección de las operaciones de modificación.

**Arquitectura:** decidir entre middleware de Express o Chain of Responsibility y eliminar las implementaciones duplicadas.

**Operación:** configurar correo real, mejorar peticiones HTTP y consultas N+1.

**Mantenimiento:** eliminar archivos y estilos de relleno, mover secretos a variables de entorno y crear pruebas.


TallerPro tiene un patrón arquitectónico real que podría aprovecharse, pero actualmente está aplicado de forma parcial. La mayor mejora sería dejar de mantener varios mecanismos de autenticación al mismo tiempo y utilizar una sola capa de protección para todas las rutas. A partir de ahí, la corrección de SQL y transacciones permitiría estabilizar los procesos que modifican información del taller.
