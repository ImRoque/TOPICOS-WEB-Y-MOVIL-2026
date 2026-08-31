# **Lenguajes**

1. Java
- Paradigma: Orientado a Objetos (OOP), Imperativo.
- Patrones de diseño: Factory, Builder, Singleton, Strategy, Observer. Altamente ligado a los patrones clásicos GoF.

2. Python
- Paradigma: Multiparadigma (OOP, Funcional, Procedimental).
- Patrones de diseño: Decorator (nativo en el lenguaje), Iterator, Strategy. Favorece el Duck Typing y la simplicidad estructural.

3. JavaScript
- Paradigma: Multiparadigma (Basado en prototipos, Funcional, Orientado a eventos).
- Patrones de diseño: Module, Observer (Eventos/Promesas), Middleware, Factory.

4. TypeScript
- Paradigma: Multiparadigma (OOP estricto, Funcional).
- Patrones de diseño: Dependency Injection, Repository, Decorator. Adopta patrones empresariales clásicos para estructurar el caos de JavaScript.

5. C#
- Paradigma: Multiparadigma (OOP, Funcional, Orientado a componentes).
- Patrones de diseño: MVVM, Unit of Work, Repository, Dependency Injection (integrada por defecto en su ecosistema).

6. Go
- Paradigma: Concurrente, Procedimental (OOP sin herencia de clases).
- Patrones de diseño: Worker Pool, Pipeline, Fan-in/Fan-out, Options Pattern. Enfoque absoluto en composición sobre herencia.

7. Rust
- Paradigma: Multiparadigma (Funcional, Imperativo, Orientado a datos).
- Patrones de diseño: RAII (Gestión de recursos por inicialización), Typestate, Builder, Newtype.

8. C++
- Paradigma: Multiparadigma (OOP, Genérico, Procedimental).
- Patrones de diseño: RAII, Pimpl (Pointer to Implementation), CRTP (Curiously Recurring Template Pattern), Singleton.

9. Ruby on Rails
- Paradigma: OOP puro, Convención sobre configuración.
- Patrones de diseño: MVC (Model-View-Controller), Active Record, Decorator/Presenter, Callback.

10. PHP / Laravel
- Paradigma: OOP, Imperativo.
- Patrones de diseño: MVC, Facade, Front Controller, Service Locator, Dependency Injection.

11. Swift
- Paradigma: Orientado a protocolos, Multiparadigma.
- Patrones de diseño: Delegate, Protocol-Oriented Patterns, MVC, MVVM, Observer (mediante Combine).

12. Kotlin
- Paradigma: Multiparadigma (OOP, Funcional).
- Patrones de diseño: Builder (nativo con bloques apply), Singleton (nativo con object), Companion Factory, Delegate.

13. Haskell
- Paradigma: Funcional puro, Evaluación perezosa (Lazy).
- Patrones de diseño: Lenses, Monads, Functors, Typeclasses. Utiliza composiciones matemáticas en lugar de flujos de control.

14. Elixir
- Paradigma: Funcional, Concurrente, Distribuido.
- Patrones de diseño: Actor Model, Supervisor, GenServer. Orientado al paso de mensajes y tolerancia a fallos.

15. Scala
- Paradigma: Híbrido puro (OOP y Funcional).
- Patrones de diseño: Cake Pattern (para inyección de dependencias), Typeclasses, Actor Model.

16. React 
- Paradigma: Declarativo, Funcional, Basado en componentes.
- Patrones de diseño: Hooks (para manejo de estado y ciclo de vida), Render Props, HOC (Higher-Order Components), Context.

17. Angular 
- Paradigma: OOP, Reactivo, Declarativo.
- Patrones de diseño: Dependency Injection, Observer (RxJS), Singleton (Servicios), MVC/MVVM.

18. Spring Boot
- Paradigma: Inversión de control, OOP.
- Patrones de diseño: Dependency Injection (IoC), Proxy, MVC, Singleton. Todo gestionado por el contexto del framework.

19. Flutter 
- Paradigma: Declarativo, Reactivo, OOP.
- Patrones de diseño: BLoC (Business Logic Component), Provider, Observer, MVC adaptado a widgets.

20. Django
- Paradigma: OOP, Procedimental.
- Patrones de diseño: MTV (Model-Template-View), Active Record, Middleware, Singleton.


# **Analisis de conflicto**

1. Rust
- Patrón incompatible: Observer con estado mutable.
- Rust es muy estricto con los datos. Si intentas que varios objetos cambien el mismo estado al mismo tiempo, el compilador te lo bloquea. Eso hace que el código se vuelva difícil de manejar y a veces termines usando soluciones raras que hacen bajar el rendimiento.

2. React
- Patrón incompatible: Orientación a Objetos con mutabilidad.
- React quiere que el estado cambie de forma controlada y sin tocarlo directo. Si haces cosas como `this.state.x = 2`, la vista no se actualiza bien y aparecen errores raros en la interfaz.

3. Go
- Patrón incompatible: MVC clásico y herencia.
- Go no tiene herencia como en Java o C#. Si intentas forzar un MVC muy rígido, se pueden crear ciclos entre archivos y paquetes, y al final el programa no compila.

4. Python
- Patrón incompatible: Inyección de dependencias estilo Java.
- Python es muy flexible y no le gusta que todo se complique. Si te obligas a crear muchas interfaces, fábricas y contenedores de dependencias, el código se pone largo, difícil y menos claro, y pierde la sencillez que Python suele tener.

5. Java
- Patrón incompatible: Programación funcional pura.
- Java sí tiene lambdas, pero forzar mucho código funcional extremo hace que el programa se vea más largo y pesado. Además, todo eso termina convirtiéndose en objetos internos y gasta más memoria.

6. JavaScript
- Patrón incompatible: Herencia clásica profunda.
- JavaScript no funciona igual que Java. Si haces muchas clases y herencias encadenadas, `this` se vuelve confuso y los métodos fallan cuando los pasas como callbacks, provocando errores en tiempo de ejecución.