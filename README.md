# Proyecto de Web Scraping - Analítica de Datos con Python Beautiful Soup, Selenium

Este proyecto contiene scripts de Python para extraer noticias de la BBC Mundo Latinoamerica, generando un CSV con título, descripción, fecha, texto completo y temas relacionados.

## Contenido
* `scraper_bs4.py`: Extracción estática usando BeautifulSoup.
* `scraper_selenium.py`: Extracción dinámica usando Selenium.
¿Cuál método usar?
	          Beautiful Soup	                 Selenium
Velocidad	   ~30 seg	                        ~90 seg
JavaScript	   No ejecuta	                   Renderiza todo
Recursos	    Liviano	                    Abre Chrome completo
Usar cuando...	El HTML ya tiene los datos	 La página carga con JS/AJAX


## Tecnologías
* Python 3, Beautifoulsoup
* selenium, Goole Chrome

## Ética
* Los datos de BBC Mundo son propiedad de BBC
* Los scripts incluyen time.sleep(2) entre solicitudes para respetar el servicio 
* Revisa siempre robors.txt antes de scrapear cualquier sitio

## Autor
Guillermo Leon Loaiza Mesa

## Instructora
Darkanita 