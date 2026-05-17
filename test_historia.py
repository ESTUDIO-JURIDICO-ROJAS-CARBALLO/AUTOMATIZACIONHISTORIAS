"""
Script de prueba: genera una historia de Instagram con el simbolo de justicia.
Ejecutar desde la carpeta del proyecto: python test_historia.py
"""
import os
import sys

# Agregar la carpeta al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bot

print("=== TEST: Generando historia con simbolo de justicia ===\n")

# Noticia de prueba
noticia_test = {
    'titulo': 'Tribunal de Córdoba dicta sentencia histórica en caso de corrupción judicial',
    'fuente': 'La Voz del Interior',
    'enlace': 'https://www.lavoz.com.ar/test',
    'dominio': 'lavoz.com.ar',
    'subtitulo': 'El Tribunal Superior de Justicia de Córdoba emitió un fallo sin precedentes que establece nuevas pautas para la transparencia en los procesos judiciales de la provincia.',
    'imagen': ''  # Se cargará automáticamente
}

print("Paso 1: Cargando símbolo de justicia...")
imagen_b64 = bot.obtener_imagen_justicia_b64()
noticia_test['imagen'] = imagen_b64
print(f"  -> Imagen cargada: {imagen_b64[:60]}...")

print("\nPaso 2: Generando imagen de historia...")
img_path = bot.crear_imagen_historia(noticia_test)
print(f"\n[OK] Historia generada exitosamente en:\n  {img_path}")
print(f"  Tamano: {os.path.getsize(img_path) / 1024:.1f} KB")
