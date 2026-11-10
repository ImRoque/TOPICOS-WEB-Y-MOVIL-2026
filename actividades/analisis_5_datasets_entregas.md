# Análisis de los datasets de entregas con árbol de decisión y random forest

Nombre: Daniel Adrian Roque Cortes  
Matrícula: 22121282  
Equipo: 5

Para esta practica entrenamos la plataforma de entregas usando seis archivos de datos diferentes con arbol de decision y random forest, las pruebas las hicimos en equipo y pusimos los porcentajes que nos dieron para ver por que cambian tanto los resultados entre cada archivo y como influyen los datos en el modelo

## Resultados del equipo

| Archivo | Arbol de decision | Random forest | Caracteristica principal |
| :--- | :---: | :---: | :--- |
| envios1.csv | 99% | 99% | Datos limpios y repartidos parejo en los 4 medios |
| envios2.csv | 76% | 80% | Meten un medio nuevo, el eskuter |
| envios3.csv | 94% | 95% | Casi todos los pedidos son en moto |
| envios4.csv | 91% | 92% | Afecta la lluvia, el viento y las horas pesadas |
| envios5.csv | 92% | 93% | Reparto variado, como un dia normal de trabajo |
| envios6.csv | 95% | 94% | Casi puras camionetas y motos, casi nada de dron ni bici |

## Explicacion de cada archivo

En envios1 los dos modelos casi no fallan porque los datos estan balanceados y los limites de peso y distancia estan muy claros, entonces es facil saber si toca bici, moto, camioneta o dron, este archivo nos sirve como base para ver como trabaja el modelo cuando los datos estan ideales

En envios2 es donde mas baja la precision porque metieron el eskuter y se enciman los rangos con la moto y la bici, al no estar bien definida la diferencia el modelo se confunde, asi que aqui la bronca no es del algoritmo sino de los datos que no separan bien la nueva opcion

En envios3 sale un porcentaje alto pero no significa que el modelo este bien entrenado, como casi todo son motos el modelo aprendio a tirar moto a casi todo y por pura estadistica le atina, pero deja fuera opciones como el dron aunque el paquete este chico, esto demuestra que un accuracy alto puede engañar si hay una clase dominante

En envios4 baja un poco el rendimiento porque entran factores como lluvia, viento y trafico, un paquete que normalmente iria en bici o dron ya no se puede mandar por ahi si hay mal clima, entonces son mas condiciones que el modelo tiene que procesar y por eso saca menos que el primer archivo

En envios5 los resultados se mantienen estables y random forest queda un poco arriba, aqui los datos estan mas mezclados entre moto, bici, camioneta y drones, por lo que se parece mucho mas a lo que pasaria en la operacion real

En envios6 el arbol salio un punto arriba de random forest, como casi todo son camionetas y motos y casi no hay casos raros como dron o bici, juntar tantos arboles no da ventaja y un solo arbol saca la chamba igual de bien

## Arbol de decision vs Random forest

Random forest salio igual o mejor en 5 de los 6 archivos, sobre todo se nota en envios2 donde las clases se cruzan porque al promediar varios arboles reduce los errores, por su parte el arbol de decision es mas ligero, rapido y facil de interpretar si necesitas explicar por que tomo esa decision

La diferencia entre los dos algoritmos fue de maximo 4%, pero entre archivos cambio mas de 20%, lo que deja claro que importa mucho mas tener datos limpios y balanceados que el modelo que uses

## Conclusion

La plataforma solo va a dar buenas recomendaciones si los datos de entrenamiento representan bien todos los medios de transporte y tienen limites claros, si una clase domina el archivo el modelo se sesga, y si metes algo nuevo sin delimitar bien como el eskuter solo vas a generar confusion

Antes de meterle mano al modelo conviene revisar el dataset y buscar que este balanceado como en envios5, ya con datos buenos el random forest conviene para tener mas precision, mientras que el arbol de decision queda bien si ocupas algo rapido y facil de explicar

