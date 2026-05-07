import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generar_nube():
    archivo = "noticias_bbc_mundo_bs4.csv"
    try:
        df = pd.read_csv(archivo)
        
        # 1. Intentamos combinar temas, títulos y descripciones para asegurar que haya texto
        temas = df['temas_relacionados'].dropna().astype(str)
        titulos = df['titulo'].dropna().astype(str)
        
        # Unimos todo en un solo bloque de texto
        texto_final = " ".join(temas) + " " + " ".join(titulos)
        
        # Verificación de seguridad
        if len(texto_final.strip()) < 10:
            print("Error: El archivo CSV parece no tener suficiente texto para analizar.")
            return

        # 2. Definimos palabras que NO queremos ver (artículos, preposiciones)
        # Esto limpia la nube de palabras como "de", "la", "que"
        stopwords_es = set(["de", "la", "el", "en", "que", "y", "los", "las", "un", "con", "para", "una", "es", "por", "del"])

        # 3. Configuramos la nube
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color='white',
            colormap='plasma',      # Un color vibrante
            stopwords=stopwords_es,
            collocations=False      # Evita que se repitan frases pegadas
        ).generate(texto_final)
        
        # 4. Crear la imagen y guardarla
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        nombre_imagen = "nube_temas_bbc.png"
        plt.savefig(nombre_imagen)
        print(f"¡Éxito! Nube de palabras generada en: {nombre_imagen}")
        plt.show()
        
    except Exception as e:
        print(f"Ocurrió un error técnico: {e}")

if __name__ == "__main__":
    generar_nube()