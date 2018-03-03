#  TMI - GRUPO 03
## DOCUMENTO DE CONCEPTO

## Título: CineBot

### Autores:

* Andrés Aguirre Juárez
* Pablo Blanco Peris
* María Castañeda López
* Maurizio Vittorini 

### Motivación del proyecto:

Estás de vacaciones, quieres ir al cine, pero no tienes idea de que salas hay cerca de ti. CineBot puede resolver el problema: al comenzar te ofrece la posibilidad de, indicándole tu ubicación muestra una lista de los cines que se encuentran más cerca de ti. Al seleccionar uno, puedes ver las películas disponibles y la programación de los pases. Además, seleccionando una película puedes acceder a más información como una breve descripción, el cartel, el reparto, la duración, etc. 
Muchas veces las páginas webs no son todo lo amigables que deberían ser. En pocos pasos vas a poder encontrar la información que necesitas e incluso enviarla a tus amigos y decidir entre todos qué película quieres ver, donde la queréis ver y cuando.

Por otra parte, nos parece interesante realizar este proyecto y así poder aprender desde cero a crear un bot.
Saber cómo crear un bot en Telegram, puede ser útil para las empresas que desean recibir comentarios de los clientes u ofrecer un servicio, o si busca una nueva forma de retenerlos y crear un acercamiento a la marca o a los servicios ofrecidos. 
Un bot puede entrar efectivamente en un plan de marketing como una herramienta para "Customer Relationship Management" (CRM): estructurado el modo de asistencia, la empresa estará en el móvil del cliente a través de la aplicación de mensajería y puede llegar con mensajes o recibir comentarios de él. 
De hecho, los bots de Telegram pueden explotarse tanto en el modo push con alerta en las noticias u ofertas, como para ser interrogados en solicitudes específicas.

### Descripción del proyecto:

Este proyecto tiene como finalidad implementar un bot para la aplicación “Telegram” que permita a los usuarios estar al día de las carteleras de los principales cines de Madrid.
Se proporcionará al usuario cierta información acerca de cada película: 

 * Una breve descripción
 * Información más detallada de la película
 * Cartel
 * Reparto
 * Director
 * Duración
 * Valoraciones
 * Últimas noticias
 * Tráiler

En la interfaz gráfica del teclado se añadirán diferentes botones descriptivos para navegar a través de la información recibida. Por ejemplo, si se selecciona una película existirán varios 
botones personalizados que actuarán como comandos.

A continuación, se detallarán los distintos comandos de los que podrás disponer en la aplicación:

 * **Buscar cine:** Busca la cartelera de un cine elegido.
 * **Buscar cine cercano:** Busca los cines más cercanos basándose en tu ubicación.
 * **Buscar película:** Busca los cines más cercanos en los que se proyecta la película.
 * **Sugerir película:** Envía la información sobre una película estrenada recientemente al azar.

Además, según el comando que se elija, aparecerán distintos botones:

 * **Buscar cine:** Se mostrará una lista de botones, asociados a cada cine. Una vez escogido el cine, nos mostrará la cartelera.

 * **Buscar cine cercano:** El bot pedirá la ubicación del usuario y mostrará una lista de los cines más cercanos a esa ubicación. Una vez escogido el cine cercano, el comportamiento será idéntico al comando anterior.

 * **Buscar película:** Mostrará una lista de películas que están en la cartelera. 

Una vez escogida la película de la cartelera, se mostrarán distintos botones relacionados con la película. 
 *  Sinopsis de la película.
 *  Fotos.
 *  Reparto.
 *  Director.
 *  Valoraciones.
 *  Últimas noticias.
 * Tráiler.

Cuando el usuario selecciona los botones de ‘Reparto’ o ‘Director’ aparecerá información relacionada con esos botones. Además, el usuario podrá tener acceso a información más detallada y películas en las que han trabajado.

### Posibles funcionalidades:

Según la complejidad de la implementación se pretenden implementar varias funcionalidades, algunas descritas anteriormente:

* Enviar un tráiler al usuario sobre la película que quiera.
* Encontrar los cines más cercanos a tu posición, con información acerca de dirección y teléfono.
* Informar sobre los precios y las promociones acerca de los pases.
* Poder acceder a la información de las películas a pesar de no estar en cartelera.

### Referencias:




