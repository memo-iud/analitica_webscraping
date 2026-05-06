"""
Taller Web Scraping - Método 2: Selenium + Beautiful Soup
Caso Práctico: BBC Mundo - Noticias de Latinoamérica
Para páginas que cargan contenido dinámicamente con JavaScript
URL: https://www.bbc.com/mundo/topics/c7zp57yyz25t
Resultado: CSV con título, descripción, fecha, texto y temas relacionados
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


BASE_URL = "https://www.bbc.com"
TOPIC_URL = f"{BASE_URL}/mundo/topics/c7zp57yyz25t"


def crear_driver():
    """Crea instancia de Chrome con opciones optimizadas para scraping."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")              # Sin interfaz gráfica
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver


def scroll_para_cargar(driver, scrolls=3, pausa=2):
    """Hace scroll hacia abajo para activar lazy loading."""
    for i in range(scrolls):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        print(f"  Scroll {i+1}/{scrolls}...")
        time.sleep(pausa)


def extraer_noticias_selenium(driver):
    """Navega a la página de listado y extrae las noticias."""
    print(f"Navegando a: {TOPIC_URL}")
    driver.get(TOPIC_URL)

    # Esperar a que cargue el contenido principal
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        print("Contenido principal cargado.")
    except Exception:
        print("Timeout esperando artículos. Intentando con el HTML actual.")

    # Scroll para cargar más noticias (lazy loading)
    scroll_para_cargar(driver, scrolls=3)

    # Pasar HTML renderizado a Beautiful Soup para parsear
    soup = BeautifulSoup(driver.page_source, "lxml")

    noticias = []

    # Buscar tarjetas de noticias
    promos = soup.find_all("div", attrs={"data-testid": re.compile("promo")})
    if not promos:
        promos = soup.find_all(
            ["article", "div"], class_=re.compile("promo|story")
        )

    print(f"Encontradas {len(promos)} noticias tras scroll dinámico")

    for promo in promos:
        noticia = {}

        # Título
        titulo_tag = promo.find(["h2", "h3"])
        noticia["titulo"] = (
            titulo_tag.get_text(strip=True) if titulo_tag else ""
        )

        # Descripción
        desc_tag = promo.find(
            "p", class_=re.compile("summary|desc|paragraph")
        )
        noticia["descripcion"] = (
            desc_tag.get_text(strip=True) if desc_tag else ""
        )

        # Fecha
        time_tag = promo.find("time")
        noticia["fecha"] = (
            time_tag.get_text(strip=True) if time_tag else ""
        )

        # URL del artículo
        link_tag = promo.find("a", href=True)
        if link_tag:
            href = link_tag["href"]
            noticia["url"] = (
                BASE_URL + href if href.startswith("/") else href
            )
        else:
            noticia["url"] = ""

        if noticia["titulo"]:
            noticias.append(noticia)

    return noticias


def extraer_articulo_selenium(driver, url):
    """Navega al artículo individual y extrae texto completo y temas."""
    try:
        driver.get(url)
        time.sleep(3)  # Esperar renderizado completo

        soup = BeautifulSoup(driver.page_source, "lxml")

        # ── Texto del artículo ──
        bloques = soup.find_all(
            attrs={"data-component": re.compile("text-block")}
        )
        if not bloques:
            art = soup.find("article") or soup.find("main")
            bloques = art.find_all("p") if art else []

        texto = "\n".join(b.get_text(strip=True) for b in bloques)

        # ── Temas relacionados ──
        temas = []
        for link in soup.find_all("a", class_=re.compile("topic|tag")):
            t = link.get_text(strip=True)
            if t and t not in temas:
                temas.append(t)

        return texto, ", ".join(temas)
    except Exception as e:
        print(f"  Error en {url}: {e}")
        return "", ""


def main():
    print("=" * 60)
    print("  SCRAPER BBC MUNDO LATINOAMÉRICA - Selenium")
    print("=" * 60)

    driver = crear_driver()
    print("Navegador Chrome iniciado en modo headless.\n")

    try:
        # Paso 1: Extraer listado de noticias
        noticias = extraer_noticias_selenium(driver)
        print(f"\nExtrayendo contenido de {len(noticias)} artículos...")

        # Paso 2: Visitar cada artículo
        for i, noticia in enumerate(noticias):
            if noticia["url"]:
                print(
                    f"  [{i+1}/{len(noticias)}] "
                    f"{noticia['titulo'][:50]}..."
                )
                texto, temas = extraer_articulo_selenium(
                    driver, noticia["url"]
                )
                noticia["texto"] = texto
                noticia["temas_relacionados"] = temas
                time.sleep(2)  # Pausa ética

        # Paso 3: Guardar en CSV
        df = pd.DataFrame(noticias)
        columnas_deseadas = [
            "titulo", "descripcion", "fecha", "texto",
            "temas_relacionados", "url"
        ]
        cols = [c for c in columnas_deseadas if c in df.columns]
        df = df[cols]

        archivo = "noticias_bbc_mundo_selenium.csv"
        df.to_csv(archivo, index=False, encoding="utf-8-sig")

        print(f"\n{'=' * 60}")
        print(f"  Guardado en: {archivo}")
        print(f"  Total: {len(df)} noticias")
        print(f"{'=' * 60}")
        print("\nVista previa:")
        print(df[["titulo", "fecha"]].to_string(index=False))

    finally:
        driver.quit()
        print("\nNavegador cerrado correctamente.")


if __name__ == "__main__":
    main()