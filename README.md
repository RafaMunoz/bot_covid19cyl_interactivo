# Telegram Bot - COVID19 CYL

Este Bot de Telegram te permite consultar y recibir alertas de una forma sencilla sobre el COVID19 en Castilla y León.
Para su funcionamiento se nutre de la API de [Datos Abiertos Castilla y León](https://datosabiertos.jcyl.es/web/es/datos-abiertos-castilla-leon.html).

Tu puedes probar este bot [aquí](https://t.me/covid19cyl_bot).

# Get Started

Este bot esta programado en Python3 y su despliegue se puede realizar a traves de Docker muy facilmente. 
Solo necesitas tener una base de datos[MongoDB 4.4.5](https://hub.docker.com/_/mongo) y este contenedor o puedes hacer uso del **docker-compose** que te dejo en el repositorio y te desplegará todo lo necesario.

## Environment variables

A continuación puede ver las variables de entorno necesarias para el funcionamiento de este contenedor.

 - **$TELEGRAM_TOKEN** -> Token de Telegram para acceder a la API HTTP del bot. 
 
 - **$URI_MONGODB**	-> URI de conexión con la base de datos MongoDB. 

 - **$ID_ADMIN** -> ID Telegram del usuario administrador.  
 
> For example: mongodb://user:pass@mongodb:27017/bc19cyl?authSource=admin


## Dataset

El bot acceso uso de los siguientes dataset de la web de [Datos Abiertos Castilla y León](https://datosabiertos.jcyl.es/web/es/datos-abiertos-castilla-leon.html).

 - [Situación epidemiológica coronavirus (COVID-19) en Castilla y León](https://analisis.datosabiertos.jcyl.es/explore/dataset/situacion-epidemiologica-coronavirus-en-castilla-y-leon)
 - [Tasa mortalidad covid por zonas básicas de salud](https://analisis.datosabiertos.jcyl.es/explore/dataset/tasa-mortalidad-covid-por-zonas-basicas-de-salud)
 - [Tasa de enfermos por zonas básicas de salud](https://analisis.datosabiertos.jcyl.es/explore/dataset/tasa-enfermos-acumulados-por-areas-de-salud)
 - [Prevalencia coronavirus](https://analisis.datosabiertos.jcyl.es/explore/dataset/prevalencia-coronavirus)
 - [Situación de hospitalizados por coronavirus en Castilla y León](https://analisis.datosabiertos.jcyl.es/explore/dataset/situacion-de-hospitalizados-por-coronavirus-en-castilla-y-leon)
 - [Ocupación de camas en hospitales](https://analisis.datosabiertos.jcyl.es/explore/dataset/ocupacion-de-camas-en-hospitales)
 - [Pruebas realizadas coronavirus](https://analisis.datosabiertos.jcyl.es/explore/dataset/pruebas-realizados-coronavirus)
 - [Fases desescalada por zonas básicas de salud](https://analisis.datosabiertos.jcyl.es/explore/dataset/fases-desescalada)
 - [Indicadores de riesgo COVID-19 por provincias](https://analisis.datosabiertos.jcyl.es/explore/dataset/indicadores-de-riesgo-covid-19-por-provincias)
 - [Vacunas recibidas COVID-19](https://analisis.datosabiertos.jcyl.es/explore/dataset/vacunas-recibidas-covid)
 - [Personas vacunadas COVID-19](https://analisis.datosabiertos.jcyl.es/explore/dataset/personas-vacunadas-covid)
