Instituto Tecnológico de Morelia Examen Diagnóstico - Fundamentos de Ingeniería de Software Materia: Tópicos Selectos de Tecnologías Web y Móvil Profesor: Jesús Eduardo Alcaraz Chávez
Nombre del Alumno: Daniel Adrián Roque Cortés 


Metodologías: ¿Cuál es la diferencia principal entre una metodología de desarrollo tradicional (como Cascada) y una metodología ágil (como Scrum) frente a los cambios en los requisitos?
Es mas complicado adaptar los cambios en la metodologia tradicional porque debido a que no pueden avanzar hasta que la primera fase o etapa este finalizada eso significaria un reinicio total o un ajuste muy lento ya que seria de etapa por etapa y no avanzaria hasta que se termine la etapa anterior, en cambio con la metodologia scrum es mas adpatable ya que se trabajan muchas fases al mismo tiempo y una actualizacion o cambio de requerimientos no sera tan complicado o tardado como en la metodologia de cascada 

Requerimientos: Explica la diferencia entre requerimientos funcionales y no funcionales, dando un ejemplo de cada uno aplicable a una plataforma web. 
Los requerimientos funcionales son operaciones que son ejecutables como un calculo, un pago, un login, etc... y un no funcionales son los que no es que se ejecuten pero se requieren por ejemplo estilos de diseño, tipo la web debe de ser unicamente colores cafe, blanco, negro y beige, no es una funcion pero si es un requerimiento...

Arquitectura: Describe el modelo Cliente-Servidor y explica brevemente cómo se comunican el frontend y el backend en una aplicación web moderna
El proyecto se separa en el backend (es donde se hacen todos los procesos) y el frontend (es todo lo visual y experiencia de usuario) y toda esa comunicacion se hace con las APIs meidante peticiones 


Bases de Datos: ¿En qué escenarios recomendarías utilizar una base de datos relacional (SQL) frente a una no relacional (NoSQL) para el almacenamiento de datos en una aplicación? 
Yo recomendaria mas SQL para apps que impliquen informacion critica ya que sql permite mejor integridad en los datos y nosql para app no tan confidenciales y que requiera mayor velocidad con poco rendimiento 

APIs: ¿Qué es una API REST y qué papel fundamental juega en la integración entre una aplicación móvil y los servidores (backend)? 
Es muy necesario un API rest en las apps porque eso permite una comunicacion mas segura con los servicios de los servidores, ya que sino todo la informacion se mandaria publicamente y eso vulnera mucho una app y como las API rest ya vienen configuradas con cierta seguridad es mil veces mejor eso 

Control de Versiones: Explica la importancia de utilizar Git en un equipo de desarrollo de software y describe brevemente qué es un "merge conflict" (conflicto de fusión).
demasiado importante ya que justo el gestion de versiones es lo mas importante ya que si trabajan en equipo mas de dos personas y de casualidad estan modificanco lo mismo o ambos se afectan haciendo cada quien lo suyo y luego uno hace push y si el otro que ya estaba trabajando hace push sin hacer pull de lo que subio su compañero a ala hora de hacer merge se generaria un conflicto ya que no trabajo uno en la version mas actualizada y si no tienen control de versiones en lugar de simplemente retroceder un commit ahora tendran que arreglar lo que hicieron y usualmente es mas complicado eso que simplemente volver a implementarlo de nuevo en la ultima version

Pruebas: ¿Qué son las pruebas unitarias (unit testing) y por qué son cruciales para asegurar la calidad del software antes de su paso a producción? 
son pruebas que no las hace un usario, lose hacen directo desde la terminal y directo en el backend y es importante para ver si todo funciona como deberia apesar de haber modificado algo

POO: Define los conceptos de encapsulamiento y polimorfismo de la Programación Orientada a Objetos, y menciona cómo ayudan a crear un código más mantenible. 
encapsular es poner es privado los datos para tener mejor control de lo que se ve o no se ve y asi no pueden modificar esos datos, el polimorfismo es reciclar metodos que se suelen usar demasiado pero en distintas formas por ejemplo un metodo reproducir() se puede usar para reproducir una cancion, reproducir una pelicula o reproducir una serie y eso hace que en lugar de generar mas metodos reproducir() usemos el mismo y asi es mas seguro que va funcionar a implementar uno nuevo cada que se requiera, ayuda mucho tambien a tener congruencia con lo que pueden hacer mis objetos 

Patrones de Diseño: ¿Qué es el patrón de arquitectura Modelo-Vista-Controlador (MVC) y cómo ayuda a organizar el código en el desarrollo de software?
no lo habia escuchado pero supongo que es la visualizacion del proyecto desde la vista del cliente para ver lo que afectamos a la hora de escribir todo y a la vez tener visible la arquitectura del proyecto para ver realmente que estamos modificando o que esta sucediendo en la terminal por posibles bugs o errores criticos o no tan criticos 

Seguridad: Explica la diferencia técnica entre "autenticación" y "autorización" en el contexto de seguridad de una aplicación.
autenticacion es verificar o validad quien eres, ya sea mediante face id, eyes id, codigo o password pero autorizacion es que cumplas ciertos requisitos por ejemplo se usa mucho para la gestion de base de datos, no todos los empleados pueden ver ciertos datos, depende el nivel gerarjico o responsabilidades que tengas en dicha empresa entonces solo los que soy gerentes o jefes de alto rango pueden ver todos los datos y a lo mejor modificar una que otra cosa pero quien puede hacer todo seria el Patron el que tiene el puesto mas alto, el podria ver, modificar, eliminar y agregar porque cumple con ese requisito, entonces la autorizacion seria que si eres empleado solo puedes ver unas cosas, si eres gerente puedes ver todo pero no modificar todo y si eres el patron puedes modificar, ver, eliminar e insertar y eso se hace mediante roles
