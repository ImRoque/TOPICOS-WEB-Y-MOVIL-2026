# Cinerex

## Situación general

Cinerex presenta una diferencia importante entre lo que se afirma en la documentación y lo que realmente implementa el proyecto. Los archivos de arquitectura hablan de logística portuaria, contenedores y grúas, mientras que la aplicación trabaja con películas, funciones, boletos y usuarios.

El problema no es únicamente documental: las reglas descritas pueden llevar a modificar o eliminar elementos que sí son necesarios para el funcionamiento de la aplicación.



### Seguridad de acceso

El mecanismo de autenticación se encuentra debilitado. Django tiene instalado su sistema de autenticación, pero `AuthenticationMiddleware` no está configurado. Además, existe una cookie `admin_bypass` que permite conceder privilegios de administrador desde el navegador. Al ser un valor controlado por el cliente, puede modificarse sin que el servidor compruebe realmente la identidad.

También existe una vista antigua (`funcion_old`) que continúa disponible y recibe parámetros directamente desde la URL.

**Corrección:** utilizar las sesiones y mecanismos de autenticación de Django, eliminar la cookie de privilegios y retirar las rutas antiguas que ya no forman parte del sistema.

### Acceso a la base de datos

Las consultas SQL se construyen concatenando información recibida del usuario. Esto aparece en el inicio de sesión, la consulta de asientos y el proceso de compra, por lo que existe un riesgo sistemático de inyección SQL.

El almacenamiento de contraseñas presenta el mismo problema de seguridad: los PIN se manejan en texto plano.

**Corrección:** migrar progresivamente al ORM de Django o, cuando sea necesario SQL directo, utilizar consultas parametrizadas. Las contraseñas deben almacenarse mediante hash y verificarse con `check_password`.

### Compra y pagos

El proceso de compra concentra demasiadas responsabilidades dentro de la vista. Ahí se calculan precios, se actualiza la base de datos, se realiza el cobro y se envía la confirmación.

El pago además construye XML manualmente y considera exitosa la operación buscando determinados caracteres en la respuesta bancaria. No existe una validación criptográfica de esa respuesta.

Otro problema es que las escrituras de boleto, asiento y puntos se realizan sin una transacción. Una falla intermedia podría dejar información inconsistente.

**Corrección:** separar la lógica de negocio de la vista, utilizar una integración de pagos segura y envolver las operaciones relacionadas de la compra en `transaction.atomic()`.

### Rendimiento y presentación

`cartelera()` genera un patrón N+1 al consultar las funciones individualmente para cada película. También realiza varias peticiones HTTP síncronas a servicios locales, haciendo que la carga dependa de todas ellas.

En `sql_cine.py` se genera HTML directamente desde Python mediante `mark_safe`, mientras que parte del contenido externo se inserta sin el escape adecuado.

**Corrección:** reducir las consultas mediante JOIN o `prefetch_related`, paralelizar o cachear las peticiones externas y dejar la generación del HTML a los templates.

### Configuración y mantenimiento

`settings.py` contiene una clave secreta débil, credenciales de base de datos, `DEBUG=True` y `ALLOWED_HOSTS=['*']`. Son configuraciones que no deberían mantenerse así fuera de desarrollo.

También existe un archivo CSS compuesto por 90 clases prácticamente iguales y no hay pruebas automatizadas para los flujos principales.

## Prioridades

1. Eliminar `admin_bypass` y restaurar la autenticación real de Django.
2. Corregir todas las consultas SQL vulnerables y dejar de almacenar contraseñas en texto plano.
3. Proteger el proceso de compra con transacciones y corregir la validación del pago.
4. Separar la lógica de negocio de las vistas.
5. Corregir las consultas N+1 y las llamadas HTTP bloqueantes.
6. Revisar configuración, salida HTML y código sin uso.
7. Rehacer la documentación para que describa Cinerex y agregar pruebas automatizadas.

El problema principal de Cinerex no es una sola falla aislada, sino la acumulación de responsabilidades dentro de las vistas y varios mecanismos de seguridad implementados de manera manual. Antes de agregar funcionalidad sería necesario estabilizar autenticación, acceso a datos y compras, ya que son las partes con mayor impacto sobre la seguridad y consistencia del sistema.
