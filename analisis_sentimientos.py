import pandas as pd
from textblob import TextBlob
import time


""""
este script no necesita conectarse a internet. 
Es mucho más rápido porque solo procesa texto que ya esta en el disco duro."""
def analizar_sentimiento(texto):
    """
    Analiza si un texto es positivo, negativo o neutro.
    Retorna la polaridad (-1 a 1).
    """
    if not texto or pd.isna(texto):
        return 0
    
    try:
        # Creamos el objeto TextBlob
        blob = TextBlob(texto)
        
        # Como TextBlob brilla en inglés, lo ideal es traducir (opcional)
        # Para este ejemplo rápido, usaremos el análisis directo 
        # (Nota: Para rigor científico en español, se usa 'textblob-es' o 'pysentimiento')
        return blob.sentiment.polarity
    except:
        return 0

def categorizar_polaridad(puntuacion):
    if puntuacion > 0.1:
        return 'Positivo'
    elif puntuacion < -0.1:
        return 'Negativo'
    else:
        return 'Neutro'

def main():
    print("Cargando datos del scraper...")
    archivo = "noticias_bbc_mundo_bs4.csv"
    
    try:
        df = pd.read_csv(archivo)
    except FileNotFoundError:
        print(f"Error: No encontré el archivo {archivo}. ¡Corre el scraper primero!")
        return

    print("Analizando sentimientos (esto puede tardar según el volumen)...")
    
    # Aplicamos el análisis a la columna 'texto' o 'descripcion'
    df['polaridad'] = df['texto'].apply(analizar_sentimiento)
    df['sentimiento'] = df['polaridad'].apply(categorizar_polaridad)

    # Guardamos el resultado
    resultado_csv = "analisis_sentimientos_bbc.csv"
    df.to_csv(resultado_csv, index=False, encoding="utf-8-sig")

    print(f"\n¡Análisis completado! Archivo guardado como: {resultado_csv}")
    
    # Mostrar resumen
    print("\nResumen de Sentimientos:")
    print(df['sentimiento'].value_counts())
    
    print("\nTop 3 Noticias más Positivas:")
    print(df.nlargest(3, 'polaridad')[['titulo', 'sentimiento']])

if __name__ == "__main__":
    main()