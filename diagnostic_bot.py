import sys
import os

# Agregar la carpeta al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import bot
    print("=== INICIANDO DIAGNÓSTICO DEL BOT ===")
    
    print("1. Buscando noticia...")
    noticia = bot.obtener_noticia_cordoba()
    if not noticia:
        print("ERROR: No se encontraron noticias válidas.")
        sys.exit(1)
    print(f"OK: Noticia encontrada: {noticia['titulo']}")
    
    print("2. Generando imagen...")
    try:
        img_path = bot.crear_imagen_historia(noticia)
        if os.path.exists(img_path):
            print(f"OK: Imagen generada en {img_path}")
            print(f"Tamaño: {os.path.getsize(img_path)} bytes")
        else:
            print("ERROR: El archivo de imagen no se creó.")
    except Exception as e:
        print(f"ERROR al generar imagen: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"ERROR CRÍTICO: {e}")
    import traceback
    traceback.print_exc()
