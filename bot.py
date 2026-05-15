import os
import time
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dotenv import load_dotenv
from html2image import Html2Image
from instagrapi import Client
from instagrapi.types import StoryLink
import base64
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Inicializar configuración
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')
load_dotenv(env_path, override=True)

USERNAME = os.getenv('IG_USERNAME')
PASSWORD = os.getenv('IG_PASSWORD')
SESSIONID = os.getenv('IG_SESSIONID')
TWO_FACTOR_CODE = os.getenv('IG_2FA_CODE')

def acortar_url(url):
    try:
        # Primero limpiamos parámetros de tracking comunes
        u = urlparse(url)
        clean_url = f"{u.scheme}://{u.netloc}{u.path}"
        if len(clean_url) < 100:
            return clean_url
        
        # Si sigue siendo larga, usamos TinyURL (gratis y sin API key para peticiones simples)
        api_url = f"http://tinyurl.com/api-create.php?url={url}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return response.text
    except Exception:
        pass
    return url

def generar_justicia_png(ruta):
    """Genera una imagen del simbolo de justicia con Pillow si no existe."""
    if not PIL_AVAILABLE:
        return False
    try:
        print("Generando simbolo de justicia con Pillow...")
        ancho, alto = 1080, 1200
        img = Image.new('RGB', (ancho, alto), color=(20, 20, 35))
        draw = ImageDraw.Draw(img)

        # Fondo con degradado oscuro azul-marino a negro
        for i in range(alto):
            ratio = i / alto
            r = int(14 + ratio * 8)
            g = int(14 + ratio * 6)
            b = int(31 + ratio * 12)
            draw.line([(0, i), (ancho, i)], fill=(r, g, b))

        # Acento magenta en la parte inferior
        for i in range(alto - 80, alto):
            ratio = (i - (alto - 80)) / 80
            draw.line([(0, i), (ancho, i)], fill=(int(229 * ratio * 0.6), 0, int(127 * ratio * 0.6)))

        # Colores
        GOLD = (212, 175, 55)
        GOLD_LIGHT = (240, 210, 100)
        GOLD_DARK = (140, 100, 20)
        MAGENTA = (229, 0, 127)

        cx = ancho // 2  # Centro horizontal

        # === Balanza de justicia mejorada ===

        # Circulo dorado en la cima
        draw.ellipse([cx - 32, 70, cx + 32, 134], fill=GOLD)
        draw.ellipse([cx - 20, 82, cx + 20, 122], fill=GOLD_DARK)
        draw.ellipse([cx - 8, 94, cx + 8, 110], fill=GOLD_LIGHT)

        # Vara central vertical (mas gruesa y definida)
        draw.rectangle([cx - 12, 102, cx + 12, 820], fill=GOLD)
        # Sombra lateral
        draw.rectangle([cx + 10, 102, cx + 15, 820], fill=GOLD_DARK)

        # Barra horizontal principal
        draw.rectangle([cx - 420, 185, cx + 420, 210], fill=GOLD)
        draw.rectangle([cx - 420, 180, cx + 420, 190], fill=GOLD_LIGHT)

        # --- Cadenas izquierdas ---
        for y in range(210, 430, 20):
            draw.ellipse([cx - 437, y, cx - 395, y + 14], outline=GOLD, width=3)
            draw.ellipse([cx - 437, y+6, cx - 395, y + 20], outline=GOLD_DARK, width=2)

        # --- Cadenas derechas ---
        for y in range(210, 430, 20):
            draw.ellipse([cx + 395, y, cx + 437, y + 14], outline=GOLD, width=3)
            draw.ellipse([cx + 395, y+6, cx + 437, y + 20], outline=GOLD_DARK, width=2)

        # --- Plato izquierdo (mas grande y detallado) ---
        px_l = cx - 416  # x izquierda del plato
        px_r = cx - 200  # x derecha del plato
        py = 428
        # Borde del plato
        draw.arc([px_l - 10, py - 10, px_r + 10, py + 60], start=0, end=180, fill=GOLD_DARK, width=6)
        # Interior del plato
        draw.arc([px_l, py, px_r, py + 50], start=0, end=180, fill=GOLD, width=10)
        # Borde superior del plato
        draw.line([(px_l - 4, py + 25), (px_r + 4, py + 25)], fill=GOLD, width=4)
        draw.line([(px_l - 8, py + 26), (px_r + 8, py + 26)], fill=GOLD_LIGHT, width=2)

        # --- Plato derecho (mismo tamano) ---
        px_l2 = cx + 200
        px_r2 = cx + 416
        draw.arc([px_l2 - 10, py - 10, px_r2 + 10, py + 60], start=0, end=180, fill=GOLD_DARK, width=6)
        draw.arc([px_l2, py, px_r2, py + 50], start=0, end=180, fill=GOLD, width=10)
        draw.line([(px_l2 - 4, py + 25), (px_r2 + 4, py + 25)], fill=GOLD, width=4)
        draw.line([(px_l2 - 8, py + 26), (px_r2 + 8, py + 26)], fill=GOLD_LIGHT, width=2)

        # --- Base (pedestal) ---
        # Trapecio
        draw.polygon([
            (cx - 110, 820), (cx + 110, 820),
            (cx + 70, 890), (cx - 70, 890)
        ], fill=GOLD)
        # Superficie de la base
        draw.rectangle([cx - 200, 885, cx + 200, 912], fill=GOLD)
        draw.rectangle([cx - 200, 880, cx + 200, 888], fill=GOLD_LIGHT)
        draw.rectangle([cx - 220, 908, cx + 220, 930], fill=GOLD_DARK)

        # --- Lineas decorativas y simbolos al pie ---
        # Linea dorada superior
        draw.rectangle([60, 960, ancho - 60, 966], fill=GOLD_DARK)
        draw.rectangle([60, 961, ancho - 61, 963], fill=GOLD_LIGHT)

        # Franja magenta central
        draw.rectangle([0, 975, ancho, 1040], fill=(30, 0, 18))
        draw.rectangle([0, 975, ancho, 978], fill=MAGENTA)
        draw.rectangle([0, 1037, ancho, 1040], fill=MAGENTA)

        # Simbolo de balanza centrado (emoji-like) con texto
        try:
            font_path = "C:/Windows/Fonts/arialbd.ttf"
            if os.path.exists(font_path):
                font_mid = ImageFont.truetype(font_path, 38)
            else:
                font_mid = ImageFont.load_default()

            texto = "CORDOBA LEGAL  |  NOTICIAS JUDICIALES"
            bbox = draw.textbbox((0, 0), texto, font=font_mid)
            tw = bbox[2] - bbox[0]
            draw.text(((ancho - tw) // 2, 990), texto, fill=GOLD, font=font_mid)
        except Exception:
            pass

        # Linea dorada inferior
        draw.rectangle([60, 1050, ancho - 60, 1056], fill=GOLD_DARK)
        draw.rectangle([60, 1051, ancho - 61, 1053], fill=GOLD_LIGHT)

        # Destellos decorativos en esquinas
        for corner_x, corner_y in [(80, 40), (ancho - 80, 40), (80, alto - 40), (ancho - 80, alto - 40)]:
            draw.ellipse([corner_x - 6, corner_y - 6, corner_x + 6, corner_y + 6], fill=GOLD)
            draw.ellipse([corner_x - 3, corner_y - 3, corner_x + 3, corner_y + 3], fill=GOLD_LIGHT)

        # Suavizado leve
        img = img.filter(ImageFilter.GaussianBlur(radius=0.8))

        img.save(ruta, 'PNG', quality=95)
        print(f"Simbolo de justicia generado: {ruta}")
        return True
    except Exception as e:
        print(f"Error generando simbolo de justicia: {e}")
        return False


def obtener_imagen_justicia_b64():
    """Obtiene el símbolo de justicia como string base64 para incrustar en HTML."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    justicia_img_path = os.path.join(base_dir, 'justicia.png')

    # Si no existe, intentamos generarla con Pillow
    if not os.path.exists(justicia_img_path):
        generado = generar_justicia_png(justicia_img_path)
        if not generado:
            # Último recurso: descargar desde internet
            try:
                print("Descargando símbolo de justicia desde internet...")
                res_img = requests.get(
                    "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=1080&q=80",
                    timeout=10
                )
                if res_img.status_code == 200:
                    with open(justicia_img_path, 'wb') as f:
                        f.write(res_img.content)
            except Exception:
                pass

    if os.path.exists(justicia_img_path):
        with open(justicia_img_path, 'rb') as f:
            data = f.read()
        ext = 'png' if justicia_img_path.endswith('.png') else 'jpeg'
        b64 = base64.b64encode(data).decode('utf-8')
        return f"data:image/{ext};base64,{b64}"
    else:
        # Fallback: imagen en línea
        return "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=1080&q=80"


def obtener_metadatos_url(url):
    subtitulo = "Deslizá hacia arriba o visita el enlace para leer los fundamentos completos de esta resolución judicial en la provincia de Córdoba."
    url_final = url
    dominio = "Fuente Original"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        session = requests.Session()
        r = session.get(url, headers=headers, timeout=15, allow_redirects=True)
        url_final = r.url

        if "news.google.com" in url_final:
            soup_tmp = BeautifulSoup(r.text, 'html.parser')
            for a in soup_tmp.find_all('a'):
                if a.get('href') and "google.com" not in a['href'] and a['href'].startswith('http'):
                    url_final = a['href']
                    r = session.get(url_final, headers=headers, timeout=15)
                    break

        dominio = urlparse(url_final).netloc.replace('www.', '')
        soup = BeautifulSoup(r.text, 'html.parser')

        # Solo extraemos la descripción, ya no buscamos imágenes de la noticia
        desc_tags = [
            {'property': 'og:description'},
            {'name': 'description'},
            {'name': 'twitter:description'}
        ]

        for tag in desc_tags:
            meta = soup.find('meta', attrs=tag)
            if meta and meta.get('content'):
                candidate = meta['content'].strip()
                if len(candidate) > 30 and not any(x in candidate.lower() for x in ['google news', 'google noticias', 'cobertura actualizada']):
                    subtitulo = candidate[:147] + "..." if len(candidate) > 150 else candidate
                    break

    except Exception as e:
        print(f"Error al obtener metadatos: {str(e)}")

    if "Google Noticias" in subtitulo or "Google News" in subtitulo:
        subtitulo = "Deslizá hacia arriba para leer los fundamentos completos de esta resolución judicial en la provincia de Córdoba."

    url_final = acortar_url(url_final)

    return subtitulo, url_final, dominio

def obtener_noticia_cordoba():
    print("Buscando noticias estrictamente legales en Google News...")
    # Búsqueda de jurisprudencia y actualidad legal en Córdoba
    query = '%28fallo+OR+sentencia+OR+justicia+OR+juez+OR+tribunal+OR+denuncia+OR+demanda%29+C%C3%B3rdoba+Argentina'
    url = f"https://news.google.com/rss/search?q={query}+when:7d&hl=es-419&gl=AR"
    feed = feedparser.parse(url)
    
    if not feed.entries:
        print("No se encontraron noticias recientes en el RSS de Google News.")
        return None
    
    print(f"Se encontraron {len(feed.entries)} noticias potenciales. Filtrando...")
    
    # Buscamos la primera noticia válida
    noticia_valida = None
    titulo_limpio = ""
    fuente = ""
    
    palabras_legales = [
        'fallo', 'juez', 'sentencia', 'fiscal', 'corte', 'tribunal', 'justicia', 
        'legal', 'abogado', 'condena', 'prisión', 'amparo', 'demanda', 'juzgado',
        'ley', 'derecho', 'juicio', 'litigio', 'penal', 'civil', 'laboral', 'familia',
        'sucesión', 'indemnización', 'recurso', 'apelación', 'suprema'
    ]
    
    fuentes_cordoba = ['la voz', 'lavoz', 'cba24n', 'el doce', 'eldoce', 'cadena 3', 'comercio y justicia', 'hoy dia cordoba', 'puntal']
    
    for entrada in feed.entries:
        titulo_completo = entrada.title
        
        # Separar la fuente del título
        if " - " in titulo_completo:
            partes = titulo_completo.rsplit(" - ", 1)
            t_limpio = partes[0]
            f_fuente = partes[1]
        else:
            t_limpio = titulo_completo
            f_fuente = "Diario Local"
            
        # Filtros para descartar noticias basura
        if any(x in t_limpio for x in ["Estamos más Cerca", "Estamos m", "Suscribite"]):
            continue
            
        if len(t_limpio.split()) < 3: 
            continue
            
        # Validación: debe contener términos legales o ser de una fuente jurídica
        texto_validar = (t_limpio + " " + (entrada.get('description', '') or '')).lower()
        es_legal = any(palabra in texto_validar for palabra in palabras_legales) or "justicia" in f_fuente.lower()
        
        if not es_legal:
            continue
            
        # Validación de ubicación: debe mencionar Córdoba o ser de una fuente local conocida
        menciona_cordoba = any(x in texto_validar for x in ["córdoba", "cordoba", "villa maría", "rio cuarto", "carlos paz"])
        es_fuente_local = any(fuente.lower() in f_fuente.lower() for fuente in fuentes_cordoba)
        
        if not (menciona_cordoba or es_fuente_local):
            continue
            
        noticia_valida = entrada
        titulo_limpio = t_limpio
        fuente = f_fuente
        break
        
    if not noticia_valida:
        print("No se encontraron noticias válidas después de filtrar estrictamente.")
        return None

    enlace = getattr(noticia_valida, 'link', '')
    print(f"Noticia encontrada: {titulo_limpio}")
    
    print("Extrayendo descripción de la noticia...")
    subtitulo, url_final, dominio = obtener_metadatos_url(enlace)

    print("Cargando simbolo de justicia...")
    imagen_b64 = obtener_imagen_justicia_b64()

    # Si el dominio sigue siendo Google News, usar la fuente periodistica
    dominio_display = dominio
    if not dominio_display or "google.com" in dominio_display or dominio_display == "Fuente Original":
        dominio_display = fuente

    return {
        "titulo": titulo_limpio,
        "fuente": fuente,
        "enlace": url_final,
        "dominio": dominio_display,
        "subtitulo": subtitulo,
        "imagen": imagen_b64
    }

def crear_imagen_historia(noticia):
    # Rutas relativas al script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'story_template.html')
    logo_path = os.path.join(base_dir, 'logo.jpg')
    temp_html_path = os.path.join(base_dir, 'temp_story.html')
    final_img_path = os.path.join(base_dir, 'story_final.png')

    print("Generando diseño de historia en PNG...")
    with open(template_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Leer el logo en base64
    logo_b64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as img_file:
            logo_b64 = base64.b64encode(img_file.read()).decode('utf-8')
            
    # Extraemos máximo 80 caracteres y lo ponemos remarcado
    titulo_corto = noticia['titulo'][:80] + ("..." if len(noticia['titulo']) > 80 else "")

    # Separar en dos para destacar la primera parte
    palabras = titulo_corto.split()
    mitad = len(palabras) // 2
    tit_destacado = " ".join(palabras[:mitad])
    tit_resto = " ".join(palabras[mitad:])

    html_tit = f"<span>{tit_destacado}</span><br>{tit_resto}"

    # La imagen del símbolo de justicia viene ya en base64 desde la noticia
    imagen_src = noticia.get('imagen', '')
    # Si por alguna razón no viene, la cargamos ahora
    if not imagen_src:
        imagen_src = obtener_imagen_justicia_b64()

    html_content = html_content.replace('{{TITLE}}', html_tit)
    html_content = html_content.replace('{{SUBTITLE}}', noticia['subtitulo'])
    html_content = html_content.replace('{{SOURCE}}', noticia['fuente'].upper())
    html_content = html_content.replace('{{LINK}}', noticia['dominio'])
    html_content = html_content.replace('{{IMAGE}}', imagen_src)
    html_content = html_content.replace('{{LOGO_B64}}', logo_b64)
    
    # Guardamos HTML temporal
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    # Convertimos a imagen
    hti = Html2Image(size=(1080, 1920), output_path=base_dir)
    # Especificamos flag para no abrir el browser de forma visible
    hti.browser.flags = ['--headless', '--disable-gpu', '--hide-scrollbars']
    
    # Usar un nombre único para evitar problemas de caché
    timestamp = int(time.time())
    filename = f'story_{timestamp}.png'
    
    print(f"Renderizando HTML a {filename}...")
    hti.screenshot(html_file=temp_html_path, save_as=filename)
    
    final_path = os.path.join(base_dir, filename)
    
    # Verificar si se creó la imagen
    if not os.path.exists(final_path):
        print(f"ERROR: No se pudo generar la imagen {filename}")
        # Intentar una vez más sin flags de browser por si acaso
        print("Reintentando sin flags adicionales...")
        hti.browser.flags = ['--headless']
        hti.screenshot(html_file=temp_html_path, save_as=filename)
        
    if os.path.exists(final_path):
        # Guardar una copia como story_final.png para la vista previa
        import shutil
        story_final_path = os.path.join(base_dir, 'story_final.png')
        shutil.copy(final_path, story_final_path)
        print(f"Imagen {final_path} generada con éxito.")
        return final_path
    else:
        raise Exception("Error crítico: Html2Image no pudo generar el archivo PNG. Revisa si Chrome/Edge está instalado.")

def publicar_en_instagram(noticia, image_path):
    if PASSWORD == "tu_contraseña_aqui":
        raise Exception("Aún no has puesto tu contraseña real en el archivo .env")
        
    print(f"Iniciando sesión en Instagram como {USERNAME}...")
    # instagrapi puede tardar unos segundos
    cl = Client()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        # Añadimos configuraciones por defecto para evitar bloqueos
        cl.delay_range = [1, 3]
        
        # Intentar cargar sesión previa para evitar bloqueos
        session_file = os.path.join(base_dir, 'session.json')
        if os.path.exists(session_file):
            print("Cargando sesión guardada...")
            cl.load_settings(session_file)
            
        if SESSIONID:
            print(f"Intentando sesión mediante SessionID ({SESSIONID[:10]}...)...")
            try:
                cl.login_by_sessionid(SESSIONID)
                print(f"Login exitoso con SessionID como: {cl.username}")
            except Exception as e:
                print(f"SessionID falló ({str(e)}). Intentando con contraseña...")
                try:
                    cl.login(USERNAME, PASSWORD, verification_code=TWO_FACTOR_CODE)
                except Exception as login_err:
                    if "two_factor" in str(login_err).lower():
                        if TWO_FACTOR_CODE:
                             raise Exception(f"El código 2FA {TWO_FACTOR_CODE} parece ser inválido o ya expiró.")
                        raise Exception("2FA_REQUIRED: Instagram requiere un código de verificación. Por favor, pásame el código que recibiste.")
                    raise login_err
        else:
            print("Iniciando sesión con contraseña...")
            try:
                cl.login(USERNAME, PASSWORD, verification_code=TWO_FACTOR_CODE)
            except Exception as login_err:
                if "two_factor" in str(login_err).lower():
                    if TWO_FACTOR_CODE:
                        raise Exception(f"El código 2FA {TWO_FACTOR_CODE} parece ser inválido o ya expiró.")
                    raise Exception("2FA_REQUIRED: Instagram requiere un código de verificación. Por favor, pásame el código que recibiste.")
                raise login_err
            
        # Verificar que la sesión es realmente válida
        try:
            profile = cl.account_info()
            print(f"Sesión validada para: {profile.username}")
            # Guardamos la sesión exitosa
            cl.dump_settings(session_file)
        except Exception as e:
            if "login_required" in str(e).lower() or "checkpoint" in str(e).lower():
                 raise Exception("CHECKPOINT_REQUIRED: Instagram bloqueó la acción. Ve a tu app y dale a 'Fui yo'. Luego intenta de nuevo.")
            print(f"La sesión se inició pero no es válida para operar: {str(e)}")
            raise e
            
        print("Subiendo historia...")
        
        links = []
        if noticia and noticia.get('enlace'):
            links.append(StoryLink(webUri=noticia['enlace']))
            
        # Parche anti-bloqueos: evitamos que la librería use la web de Instagram para buscar datos
        if hasattr(cl, 'user_id') and cl.user_id:
            cl.user_short_gql = lambda user_id: {"pk": cl.user_id, "username": USERNAME, "full_name": USERNAME, "profile_pic_url": ""}
            
        cl.photo_upload_to_story(
            path=image_path,
            caption="Nuevo caso legal #CórdobaLegal #EstudioJuridico",
            links=links
        )
        print("Historia publicada con éxito!")
    except Exception as e:
        error_msg = str(e)
        if "challenge" in error_msg.lower() or "checkpoint" in error_msg.lower():
            raise Exception("Instagram bloqueó el inicio de sesión. Revisa tu app de Instagram en el celular y confirma que fuiste tú. Luego intenta de nuevo.")
        elif "password" in error_msg.lower():
            raise Exception("Contraseña incorrecta. Revisa el archivo .env.")
        else:
            raise Exception(f"Error de Instagram: {error_msg}")

if __name__ == "__main__":
    print("=== INICIANDO BOT DE STORIES ROJAS & CARBALLO ===")
    noticia = obtener_noticia_cordoba()
    if noticia:
        img_path = crear_imagen_historia(noticia)
        publicar_en_instagram(noticia, img_path)
        print("\n¡Proceso completado con éxito!")
    else:
        print("No hay noticias hoy.")
        
