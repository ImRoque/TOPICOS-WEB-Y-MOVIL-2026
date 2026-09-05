# PasoFit

## Estado de la arquitectura

PasoFit cuenta con dependencias para `flutter_bloc` y `provider` e incluso tiene un Cubit, pero las pantallas principales utilizan un sistema de eventos creado manualmente. La documentación establece que este tipo de listas de oyentes no debería utilizarse, por lo que existe una contradicción directa entre la arquitectura declarada y la implementación.

Además, la documentación identifica la aplicación como un sistema bancario cuando el código corresponde a una app de entrenamiento.

## Problemas que afectan al funcionamiento

### Estado y ciclo de vida

`RelojBus` y `PesoBus` mantienen listas estáticas de listeners. Los callbacks registrados desde las pantallas no se eliminan al salir mediante `dispose()`.

Cada nueva entrada a esas pantallas puede acumular otro listener, provocando consumo innecesario de memoria y actualizaciones de widgets que ya no deberían recibir eventos.

**Solución:** utilizar un único mecanismo de manejo de estado y controlar correctamente el ciclo de vida de los suscriptores.

### Autenticación

El login envía usuario y contraseña a través de HTTP sin TLS. La aplicación determina el resultado revisando fragmentos del cuerpo de la respuesta y, además, utiliza un identificador de usuario fijo al navegar.

La pantalla de inicio tampoco realiza una comprobación de sesión confiable.

**Solución:** utilizar HTTPS, una respuesta estructurada del servidor y conservar la identidad real de la sesión. Si la sesión no es válida, el flujo debe regresar al login.

### SQLite dentro de la interfaz

Las pantallas de rutina, peso y logros realizan directamente consultas a SQLite desde el `State`. Algunas consultas se construyen mediante interpolación de valores.

Esto rompe la separación de responsabilidades que plantea la propia arquitectura y hace que los widgets conozcan detalles de persistencia.

**Solución:** crear un repositorio que concentre el acceso a `sqflite` y utilizar parámetros en las consultas. La interfaz debe trabajar con datos y operaciones del dominio, no con SQL.

### Carga de datos

`inicio.dart` realiza múltiples peticiones HTTP locales al cargar la pantalla y utiliza bloques `try/catch` que simplemente ignoran los errores.

Esto puede hacer que la interfaz espere innecesariamente y, al mismo tiempo, ocultar la causa de una falla.

**Solución:** utilizar `Future.wait`, establecer timeouts y registrar los errores para poder diagnosticarlos.

### Lógica de entrenamiento y mantenimiento

El gasto de kilocalorías se determina mediante valores fijos dentro de `RutinaPantalla`, mezclando lógica de negocio con UI. `rutina.dart` también fuerza el tipo de los argumentos de navegación sin validar su contenido.

`rutina_old.dart` no se utiliza y debe considerarse código muerto.

Finalmente, no existen pruebas automatizadas para login, rutinas o peso.

## Priodidades

- Sustituir el bus de eventos manual por un mecanismo de estado único.
- Corregir el ciclo de vida de los listeners.
- Asegurar el login y la validación de sesión.
- Crear el repositorio para SQLite y parametrizar las consultas.
- Sacar los cálculos de calorías de los widgets.
- Eliminar `rutina_old.dart`.
- Agregar pruebas de los flujos principales.
- Actualizar la documentación para que corresponda con la aplicación real.

PasoFit no presenta únicamente errores puntuales en las pantallas; el problema central está en la separación de responsabilidades. La UI controla estado, navegación, persistencia y parte de la lógica de negocio al mismo tiempo. La solución más conveniente es establecer una arquitectura clara y aprovechar las herramientas que el proyecto ya tiene declaradas en lugar de mantener mecanismos paralelos.
