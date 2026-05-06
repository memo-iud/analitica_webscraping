"""
Taller Web Scraping - Método 1: Beautiful Soup
Caso Práctico: BBC Mundo - Noticias de Latinoamérica
URL: https://www.bbc.com/mundo/topics/c7zp57yyz25t
Resultado: CSV con título, descripción, fecha, texto y temas relacionados
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# ── Configuración ──
BASE_URL = "https://www.bbc.com"
TOPIC_URL = f"{BASE_URL}/mundo/topics/c7zp57yyz25t"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9",
}


def obtener_pagina(url):
    """Realiza GET request y retorna objeto BeautifulSoup."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return None


def extraer_noticias_listado(soup):
    """Extrae títulos, descripciones, fechas y URLs del listado de noticias."""
    noticias = []

    # BBC usa elementos con atributos data-testid para tarjetas de noticias
    promos = soup.find_all("div", attrs={"data-testid": re.compile("promo")})

    # Fallback: buscar por clase CSS
    if not promos:
        promos = soup.find_all("div", class_=re.compile("promo"))

    # Fallback 2: buscar bloques de artículo
    if not promos:
        promos = soup.find_all(
            ["article", "li"], class_=re.compile("promo|story|item")
        )

    print(f"Encontradas {len(promos)} tarjetas de noticias")

    for promo in promos:
        noticia = {}

        # ── Título ──
        titulo_tag = promo.find(
            ["h2", "h3"], class_=re.compile("heading|title|promo")
        )
        if not titulo_tag:
            titulo_tag = promo.find(["h2", "h3"])
        noticia["titulo"] = titulo_tag.get_text(strip=True) if titulo_tag else ""

        # ── Descripción ──
        desc_tag = promo.find(
            "p", class_=re.compile("summary|description|paragraph")
        )
        noticia["descripcion"] = desc_tag.get_text(strip=True) if desc_tag else ""

        # ── Fecha / Tiempo de publicación ──
        time_tag = promo.find("time")
        if time_tag:
            noticia["fecha"] = time_tag.get_text(strip=True)
            noticia["datetime"] = time_tag.get("datetime", "")
        else:
            span_time = promo.find(
                "span", class_=re.compile("date|time|timestamp")
            )
            noticia["fecha"] = (
                span_time.get_text(strip=True) if span_time else ""
            )
            noticia["datetime"] = ""

        # ── URL del artículo ──
        link_tag = promo.find("a", href=True)
        if link_tag:
            href = link_tag["href"]
            if href.startswith("/"):
                href = BASE_URL + href
            noticia["url"] = href
        else:
            noticia["url"] = ""

        # Solo agregar si tiene título
        if noticia["titulo"]:
            noticias.append(noticia)

    return noticias


def extraer_articulo(url):
    """Entra al artículo individual y extrae texto completo y temas."""
    soup = obtener_pagina(url)
    if not soup:
        return "", ""

    # ── Texto del artículo ──
    # BBC usa data-component="text-block" para los párrafos
    bloques_texto = soup.find_all(
        attrs={"data-component": re.compile("text-block|subheadline")}
    )

    if not bloques_texto:
        # Alternativa: buscar en el contenedor principal
        article_body = soup.find("article") or soup.find("main")
        if article_body:
            bloques_texto = article_body.find_all("p")

    texto = "\n".join(b.get_text(strip=True) for b in bloques_texto)

    # ── Temas relacionados ──
    temas_section = soup.find("div", class_=re.compile("topic|tag|related"))
    temas = []
    if temas_section:
        for tag_link in temas_section.find_all("a"):
            tema = tag_link.get_text(strip=True)
            if tema and tema not in temas:
                temas.append(tema)

    # Fallback: buscar enlaces de tema individuales
    if not temas:
        for link in soup.find_all("a", class_=re.compile("topic|tag")):
            tema = link.get_text(strip=True)
            if tema and tema not in temas:
                temas.append(tema)

    return texto, ", ".join(temas)


def main():
    print("=" * 60)
    print("  SCRAPER BBC MUNDO LATINOAMÉRICA - Beautiful Soup")
    print("=" * 60)

    # Paso 1: Obtener la página de listado
    print(f"\nAccediendo a: {TOPIC_URL}")
    soup = obtener_pagina(TOPIC_URL)
    if not soup:
        print("No se pudo acceder a la página. Terminando.")
        return

    # Paso 2: Extraer noticias del listado
    noticias = extraer_noticias_listado(soup)
    print(f"Se extrajeron {len(noticias)} noticias del listado")

    # Paso 3: Visitar cada artículo para obtener texto completo y temas
    print("\nExtrayendo texto completo de cada artículo...")
    for i, noticia in enumerate(noticias):
        if noticia["url"]:
            print(f"  [{i+1}/{len(noticias)}] {noticia['titulo'][:50]}...")
            texto, temas = extraer_articulo(noticia["url"])
            noticia["texto"] = texto
            noticia["temas_relacionados"] = temas
            time.sleep(2)  # Pausa ética entre solicitudes

    # Paso 4: Crear DataFrame y guardar CSV
    df = pd.DataFrame(noticias)
    columnas_deseadas = [
        "titulo", "descripcion", "fecha", "texto",
        "temas_relacionados", "url"
    ]
    columnas_existentes = [c for c in columnas_deseadas if c in df.columns]
    df = df[columnas_existentes]

    archivo_csv = "noticias_bbc_mundo_bs4.csv"
    df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")

    print(f"\n{'=' * 60}")
    print(f"  Datos guardados en: {archivo_csv}")
    print(f"  Total de noticias: {len(df)}")
    print(f"  Columnas: {list(df.columns)}")
    print(f"{'=' * 60}")
    print("\nVista previa:")
    print(df[["titulo", "fecha"]].to_string(index=False))


if __name__ == "__main__":
    main()