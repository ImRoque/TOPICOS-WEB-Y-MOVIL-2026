# Hotel Luna

## Lectura del proyecto

Hotel Luna es una aplicación Spring Boot para reservaciones, pero sus documentos de arquitectura todavía describen un inventario de piezas de la NASA. La diferencia llega al punto de afirmar que determinadas tablas no deben existir cuando son precisamente las que utiliza la aplicación.

La documentación también da por hecho que Spring Security y `@Transactional` están funcionando, aunque la implementación real demuestra lo contrario.

## Lo que está ocurriendo en la aplicación

### El flujo de Spring está siendo interferido

`FrontControllerServlet` está registrado sobre `/*`, por lo que compite con el `DispatcherServlet` de Spring MVC. Esto rompe la separación normal de responsabilidades del framework.

A esto se suma una cadena de filtros casera que realmente no tiene filtros configurados. El resultado es una arquitectura con componentes que aparentan controlar las peticiones, pero que no realizan esa función de manera efectiva.

**Recomendación:** dejar a Spring MVC como responsable del despacho y utilizar mecanismos estándar para interceptar y proteger las peticiones.

### Autenticación implementada fuera de Spring Security

Aunque `spring-boot-starter-security` aparece como dependencia, el inicio de sesión se realiza manualmente en `LoginCtrl`. La consulta concatena correo y contraseña y la autorización administrativa depende de `admin_bypass`.

Esto permite dos problemas simultáneos: inyección SQL y manipulación de privilegios desde el navegador. Las claves tampoco se manejan mediante un hash seguro.

**Recomendación:** configurar Spring Security de forma efectiva, utilizar `PasswordEncoder`, sesiones controladas por el servidor y eliminar el mecanismo de cookie administrativa.

### Reservaciones sin unidad transaccional

La creación de una reservación modifica diferentes elementos relacionados, como la reserva, la habitación y los servicios adicionales. Estas operaciones no están protegidas por una transacción real.

Si una operación falla después de que otra ya fue realizada, la base de datos puede quedar en un estado parcialmente actualizado.

Los precios, además, se deciden mediante condicionales dentro del controlador, mezclando reglas del negocio con la recepción de peticiones.

**Recomendación:** colocar la operación en una capa de servicio y utilizar `@Transactional`; las tarifas deben mantenerse fuera del controlador.

### Consultas y generación de contenido

`FacturaSql` vuelve a consultar información de spa por cada reserva, generando N+1. Además, utiliza valores concatenados en SQL.

El resultado se entrega mediante `th:utext`, que evita el escape automático de Thymeleaf y abre la posibilidad de XSS si el contenido llega a estar controlado por un usuario.

**Recomendación:** resolver los datos mediante JOIN y parámetros, y utilizar `th:text` para la salida normal.

### Peticiones externas y configuración

La página principal crea un `RestTemplate` en cada petición y realiza varias llamadas internas de manera síncrona. Los errores son descartados.

El pago sigue un esquema parecido al de otros procesos del proyecto: XML construido manualmente y una respuesta considerada válida mediante una búsqueda de texto, sin firma criptográfica.

Por otro lado, `application.properties` contiene credenciales de MySQL y la base de datos no refleja una estrategia segura para almacenar contraseñas.

## Prioridades

**Primero:** eliminar el conflicto del `FrontControllerServlet` y configurar Spring Security.

**Después:** eliminar `admin_bypass`, parametrizar las consultas y migrar el manejo de contraseñas a `PasswordEncoder`.

**Luego:** hacer transaccional la creación de reservaciones y separar las tarifas de los controladores.

**Finalmente:** resolver N+1, mejorar las llamadas HTTP, corregir la salida HTML, retirar el CSS de relleno y crear pruebas para login, reservaciones y tarifas.

Hotel Luna tiene una base funcional reconocible, pero actualmente utiliza componentes de Spring junto con soluciones caseras que terminan anulando parte de sus ventajas. La corrección debe centrarse en recuperar los mecanismos propios del framework antes de seguir aumentando la funcionalidad.
