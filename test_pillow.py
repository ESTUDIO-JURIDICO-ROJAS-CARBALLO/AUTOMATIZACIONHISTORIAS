import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def descargar_fuentes():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_montserrat_bold = os.path.join(base_dir, 'Montserrat-Bold.ttf')
    font_montserrat_medium = os.path.join(base_dir, 'Montserrat-Medium.ttf')
    
    if not os.path.exists(font_montserrat_bold):
        try:
            url = "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Bold.ttf"
            print(f"Descargando Montserrat-Bold.ttf desde {url}...")
            r = requests.get(url, timeout=20)
            print(f"Status Code Montserrat-Bold: {r.status_code}")
            if r.status_code == 200:
                with open(font_montserrat_bold, 'wb') as f:
                    f.write(r.content)
                print("Montserrat-Bold guardado con exito.")
            else:
                print(f"Error: Status code {r.status_code}")
        except Exception as e:
            print(f"Error descargando Montserrat-Bold: {e}")
            
    if not os.path.exists(font_montserrat_medium):
        try:
            url = "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/fonts/ttf/Montserrat-Medium.ttf"
            print(f"Descargando Montserrat-Medium.ttf desde {url}...")
            r = requests.get(url, timeout=20)
            print(f"Status Code Montserrat-Medium: {r.status_code}")
            if r.status_code == 200:
                with open(font_montserrat_medium, 'wb') as f:
                    f.write(r.content)
                print("Montserrat-Medium guardado con exito.")
            else:
                print(f"Error: Status code {r.status_code}")
        except Exception as e:
            print(f"Error descargando Montserrat-Medium: {e}")

def quitar_emojis(texto):
    """Elimina emojis y caracteres especiales no soportados por fuentes estándar."""
    import re
    # Dejar solo caracteres latinos imprimibles y puntuación básica
    clean_text = re.sub(r'[^\w\s\d.,!?;:()""\'\'\-áéíóúÁÉÍÓÚñÑüÜ|]', '', texto)
    # Reemplazar múltiples espacios por uno solo
    return re.sub(r'\s+', ' ', clean_text).strip()

def wrap_text(text, font, max_width, draw):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def crear_imagen_historia_pillow(noticia):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, 'logo.jpg')
    justicia_img_path = os.path.join(base_dir, 'justicia.png')
    
    # Descargar fuentes si no existen
    descargar_fuentes()
    
    # Cargar fuentes
    font_m_bold = os.path.join(base_dir, 'Montserrat-Bold.ttf')
    font_m_medium = os.path.join(base_dir, 'Montserrat-Medium.ttf')
    
    if os.path.exists(font_m_bold):
        font_topbar = ImageFont.truetype(font_m_bold, 36)
        font_montserrat_badge = ImageFont.truetype(font_m_bold, 32)
        font_montserrat_title = ImageFont.truetype(font_m_bold, 54)
        font_montserrat_source = ImageFont.truetype(font_m_bold, 32)
    else:
        font_topbar = ImageFont.load_default()
        font_montserrat_badge = ImageFont.load_default()
        font_montserrat_title = ImageFont.load_default()
        font_montserrat_source = ImageFont.load_default()
        
    if os.path.exists(font_m_medium):
        font_inter_sub = ImageFont.truetype(font_m_medium, 34)
        font_inter_label = ImageFont.truetype(font_m_medium, 22)
        font_inter_link = ImageFont.truetype(font_m_medium, 26)
    else:
        font_inter_sub = ImageFont.load_default()
        font_inter_label = ImageFont.load_default()
        font_inter_link = ImageFont.load_default()

    # Limpiar textos de emojis antes de dibujar
    titulo_limpio = quitar_emojis(noticia['titulo'])
    subtitulo_limpio = quitar_emojis(noticia['subtitulo'])
    fuente_limpia = quitar_emojis(noticia['fuente'])
    
    # 1. Crear Canvas (1080 x 1920)
    bg = Image.new('RGBA', (1080, 1920), (240, 240, 240, 255))
    draw = ImageDraw.Draw(bg)
    
    # 2. Agregar marca de agua sutil de fondo
    if os.path.exists(justicia_img_path):
        try:
            watermark = Image.open(justicia_img_path).convert('RGBA')
            # Cover logic: resize keeping aspect ratio or fit
            watermark.thumbnail((1080, 1920), Image.Resampling.LANCZOS)
            # Create a larger canvas to center the watermark if needed
            watermark_full = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
            wx = (1080 - watermark.width) // 2
            wy = (1920 - watermark.height) // 2
            watermark_full.paste(watermark, (wx, wy))
            
            # Ajustar la opacidad al 15%
            r, g, b, a = watermark_full.split()
            a = a.point(lambda p: int(p * 0.15))
            watermark_full = Image.merge('RGBA', (r, g, b, a))
            bg.alpha_composite(watermark_full)
        except Exception as e:
            print(f"Error cargando marca de agua: {e}")

    # 3. Topbar "CÓRDOBA LEGAL"
    draw.text((70, 50), "CORDOBA LEGAL", fill=(229, 0, 127, 255), font=font_topbar)
    
    # 4. Caja destacada (Featured Box)
    # Fondo oscuro
    draw.rounded_rectangle([70, 130, 1010, 690], radius=24, fill=(20, 20, 31, 255), outline=(229, 0, 127, 255), width=4)
    
    # Balanza centrada
    if os.path.exists(justicia_img_path):
        try:
            justicia_box = Image.open(justicia_img_path).convert('RGBA')
            justicia_box.thumbnail((900, 480), Image.Resampling.LANCZOS)
            jx = 70 + (940 - justicia_box.width) // 2
            jy = 130 + (560 - justicia_box.height) // 2
            bg.paste(justicia_box, (jx, jy), justicia_box)
        except Exception as e:
            print(f"Error pegando balanza: {e}")
            
    # Overlay magenta al fondo de la caja
    draw.rectangle([74, 610, 1006, 686], fill=(157, 0, 86, 220))
    
    # Texto "NOTICIA DESTACADA"
    text_badge = "NOTICIA DESTACADA"
    bbox = draw.textbbox((0, 0), text_badge, font=font_montserrat_badge)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((70 + (940 - tw) // 2, 610 + (76 - th) // 2 - 4), text_badge, fill=(255, 255, 255, 255), font=font_montserrat_badge)

    # 5. Título de la noticia
    title_wrapped = wrap_text(titulo_limpio.upper(), font_montserrat_title, 940, draw)
    y_curr = 740
    for line in title_wrapped[:3]: # Limitar a 3 líneas para evitar desborde
        draw.text((70, y_curr), line, fill=(157, 0, 86, 255), font=font_montserrat_title)
        y_curr += 68

    # 6. Subtítulo (con barra vertical decorativa)
    y_curr += 30
    sub_wrapped = wrap_text(subtitulo_limpio, font_inter_sub, 880, draw)
    y_sub_start = y_curr
    for line in sub_wrapped[:4]: # Limitar a 4 líneas
        draw.text((100, y_curr), line, fill=(59, 28, 42, 255), font=font_inter_sub)
        y_curr += 48
    y_sub_end = y_curr - 12
    
    # Línea vertical magenta gruesa
    draw.line([(73, y_sub_start + 4), (73, y_sub_end)], fill=(157, 0, 86, 255), width=8)

    # 7. Tarjeta de fuente
    y_curr += 35
    draw.rounded_rectangle([70, y_curr, 1010, y_curr + 180], radius=16, fill=(255, 255, 255, 255), outline=(209, 213, 219, 255), width=2)
    draw.text((105, y_curr + 22), "FUENTE DE LA INFORMACION", fill=(156, 163, 175, 255), font=font_inter_label)
    draw.text((105, y_curr + 58), fuente_limpia.upper(), fill=(31, 41, 55, 255), font=font_montserrat_source)
    draw.text((105, y_curr + 108), noticia['dominio'], fill=(157, 0, 86, 255), font=font_inter_link)

    # 8. Contenedor de Logo (Footer fijo abajo)
    draw.rounded_rectangle([140, 1590, 940, 1830], radius=28, fill=(255, 255, 255, 255), outline=(157, 0, 86, 255), width=5)
    
    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert('RGBA')
            logo.thumbnail((650, 180), Image.Resampling.LANCZOS)
            lx = 140 + (800 - logo.width) // 2
            ly = 1590 + (240 - logo.height) // 2
            bg.paste(logo, (lx, ly), logo)
        except Exception as e:
            print(f"Error pegando logo: {e}")

    # Guardar imagen final
    final_img_path = os.path.join(base_dir, 'story_pillow_test.png')
    bg.convert('RGB').save(final_img_path, 'PNG', quality=95)
    print(f"Imagen generada con Pillow en: {final_img_path}")
    return final_img_path

# Ejecutar test
if __name__ == "__main__":
    noticia_test = {
        'titulo': 'El Tribunal Superior de Justicia de Córdoba institucionalizó el ingreso por mérito tras 30 años de reforma',
        'fuente': 'Justicia Córdoba',
        'enlace': 'https://www.justiciacordoba.gob.ar/test',
        'dominio': 'justiciacordoba.gob.ar',
        'subtitulo': 'Se cumplen tres décadas del histórico fallo de la Sala Constitucional que marcó un hito en la transparencia de los concursos para el Poder Judicial provincial.',
    }
    crear_imagen_historia_pillow(noticia_test)
