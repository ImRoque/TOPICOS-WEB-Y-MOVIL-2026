# Sabores del Barrio

## Panorama del sistema

El proyecto corresponde a una plataforma de pedidos de comida, pero su documentación describe un sistema gubernamental de censo y traslado de ganado. Incluso las entidades que la documentación prohíbe son las mismas que la aplicación necesita para funcionar.

Esta diferencia afecta también a las decisiones arquitectónicas, porque se afirma que Laravel ya tiene protegidas las rutas cuando en realidad los middlewares están definidos pero no aplicados.

## Riesgos principales

### Identidad del usuario

El problema más delicado de `PedidoController` es que el servidor acepta `id_cliente` desde el formulario. El identificador puede modificarse antes de enviarlo, permitiendo realizar operaciones a nombre de otro usuario.

La cookie `admin_bypass` presenta un problema similar: el servidor confía en un dato que el cliente puede alterar.

**Solución:** obtener la identidad exclusivamente de la sesión autenticada y eliminar cualquier mecanismo de privilegios basado en cookies libres.

### SQL y acceso a datos

El login concatena los valores recibidos en una consulta SQL. También existen consultas vulnerables en pedidos y reseñas.

El problema se agrava porque algunas vistas Blade abren conexiones `mysqli` directamente, mantienen sus propias credenciales y ejecutan consultas desde la capa de presentación.

`/menu_old` continúa activo y representa otro punto de entrada con SQL interpolado y salida sin escape.

**Solución:** concentrar el acceso a datos en modelos/controladores utilizando Eloquent o `DB`, parametrizar las consultas y retirar las rutas antiguas.

### Pago y formularios

El pago transmite el número de tarjeta directamente hacia una pasarela mediante XML construido manualmente. La respuesta se considera correcta buscando una cadena determinada, sin una validación criptográfica.

Además, el formulario de pago no utiliza `@csrf`, a diferencia de otros formularios del proyecto.

**Solución:** utilizar tokenización mediante un proveedor de pagos certificado, validar las respuestas con el mecanismo de firma correspondiente y agregar protección CSRF a todos los POST.

### Rendimiento y consistencia

`HomeController` genera consultas N+1 para obtener información de los restaurantes y realiza varias llamadas HTTP bloqueantes. Los errores se silencian mediante `@`.

El cierre de reparto modifica diferentes registros sin una transacción y utiliza `mail()` directamente.

**Solución:** reducir las consultas, paralelizar o cachear llamadas externas, registrar errores y utilizar `DB::transaction()` junto con el sistema de correo de Laravel, preferentemente con colas.

### Mantenimiento

`FrontController.php` intenta duplicar el sistema de rutas de Laravel, pero no está conectado al flujo real. También existe un CSS con numerosas clases prácticamente idénticas y no hay pruebas automatizadas.

El `.env` incluido contiene credenciales de base de datos y no debería formar parte del repositorio.

## Prioridades

La primera etapa debería centrarse en **autenticación y autorización**. Después deben corregirse las consultas SQL y el acceso a datos desde las vistas. Posteriormente deben asegurarse los pagos, CSRF y las operaciones transaccionales.

Una vez controlados estos riesgos, conviene atacar rendimiento, código muerto, configuración y pruebas.

Sabores del Barrio conserva buena parte de los mecanismos propios de Laravel, pero varios de ellos fueron reemplazados por soluciones manuales o simplemente quedaron sin aplicar. El principal objetivo debería ser volver a utilizar el flujo estándar del framework y evitar que el cliente determine identidad, permisos o información sensible.
