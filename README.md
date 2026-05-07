🕵️‍♂️ Web Scraping & Data Analysis: BBC Mundo
Este proyecto realiza un ciclo completo de analítica de datos: desde la extracción automatizada de noticias hasta el procesamiento de lenguaje natural (NLP) para medir sentimientos y tendencias.

🚀 Módulos del Proyecto
Extracción (Scraping)
scraper_bs4.py: Extracción estática de alto rendimiento.

scraper_selenium.py: Extracción dinámica para contenido renderizado con JavaScript.

	          Beautiful Soup	                 Selenium
Velocidad	   ~30 seg	                        ~90 seg
JavaScript	   No ejecuta	                   Renderiza todo
Recursos	    Liviano	                    Abre Chrome completo
Usar cuando...	El HTML ya tiene los datos	 La página carga con JS/AJAX

Inteligencia de Datos (NLP)
analisis_sentimientos.py: Implementa TextBlob para clasificar las noticias en Positivas, Negativas o Neutras basándose en la polaridad del texto.

relacionados_temas.py: Genera una Nube de Palabras (WordCloud) analizando la frecuencia de temas y títulos para identificar tendencias globales.

📊 Visualización de Tendencias
El proyecto genera automáticamente una representación visual de los temas más candentes en la BBC Mundo:

🛠️ Tecnologías y Librerías
Procesamiento: Python 3.12, Pandas

Scraping: BeautifulSoup4, Selenium

IA/NLP: TextBlob

Gráficos: Matplotlib, WordCloud

⚖️ Ética y Buenas Prácticas
Respeto al Servidor: Los scripts incluyen time.sleep(2) para evitar sobrecargar los servidores de la BBC.

Propiedad Intelectual: Los datos extraídos son propiedad de la BBC; este proyecto tiene fines académicos.

Transparencia: Se recomienda revisar siempre el archivo robots.txt del sitio objetivo.

👥 Créditos
Autor: Guillermo Leon Loaiza Mesa

Instructora: Darkanita

Materia: Programación para Analítica de Datos