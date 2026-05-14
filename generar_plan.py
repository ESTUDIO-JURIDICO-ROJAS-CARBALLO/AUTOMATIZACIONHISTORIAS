import os
import datetime
from html2image import Html2Image

PLAN_PUBLICACION = [
    {
        "tema": "Derecho Laboral",
        "texto": "3 cosas que NO sabías sobre la Ley de Riesgos del Trabajo en Argentina. 🚧",
        "imagen": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800&q=80"
    },
    {
        "tema": "Derecho de Familia",
        "texto": "Divorcio Express en 2026: Requisitos y Tiempos Actuales. ⏳",
        "imagen": "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80"
    },
    {
        "tema": "Derecho Laboral",
        "texto": "¿Estás anotado bajo 'tiempo parcial' (media jornada) pero trabajás 8 horas o más? 🕒🚨",
        "imagen": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&q=80"
    },
    {
        "tema": "Derecho de Familia",
        "texto": "Mitos y Verdades sobre la Cuota Alimentaria y el Divorcio. 💸",
        "imagen": "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&q=80"
    },
    {
        "tema": "Derecho Laboral",
        "texto": "Nueva Ley de Bases: ¿Cómo me afecta ahora el 'Período de Prueba'? 🔍",
        "imagen": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&q=80"
    },
    {
        "tema": "Institucional",
        "texto": "Detrás de cada expediente, hay una persona buscando justicia. 💼",
        "imagen": "https://images.unsplash.com/photo-1505664159854-2326182735ce?w=800&q=80"
    },
    {
        "tema": "Derecho Laboral",
        "texto": "Me echaron sin causa después de 10 años. Gracias al Estudio cobré mi indemnización completa. 🤝",
        "imagen": "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800&q=80"
    },
    {
        "tema": "Derecho de Familia",
        "texto": "¿La otra parte no quiere firmar el divorcio? 🚫✍️",
        "imagen": "https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=800&q=80"
    },
    {
        "tema": "Derecho Laboral",
        "texto": "3 Documentos que SIEMPRE debés pedir al firmar un contrato laboral. 📑",
        "imagen": "https://images.unsplash.com/photo-1603796846027-ea4ea4e3759c?w=800&q=80"
    },
    {
        "tema": "Derecho de Familia",
        "texto": "División de bienes tras el divorcio: No pierdas lo que te corresponde. 🏠🚗",
        "imagen": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&q=80"
    },
    {
        "tema": "Derecho Laboral",
        "texto": "'Recibí un telegrama de despido'. ¿Qué es lo primero que debo hacer? 📬",
        "imagen": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=800&q=80"
    },
    {
        "tema": "Institucional",
        "texto": "Estudio Jurídico Rojas & Carballo. Tu respaldo legal en Córdoba. ⚖️",
        "imagen": "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800&q=80"
    }
]

def crear_imagen(index, post, fecha):
    with open('story_template.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    titulo_corto = post['tema']
    
    html_tit = f"<span>{titulo_corto}</span><br>Rojas & Carballo"
    
    fuente_fecha = f"{fecha} • ESTUDIO JURÍDICO"
    
    html_content = html_content.replace('{{TITLE}}', html_tit)
    html_content = html_content.replace('{{SUBTITLE}}', post['texto'])
    html_content = html_content.replace('{{SOURCE}}', fuente_fecha.upper())
    html_content = html_content.replace('{{LINK}}', 'Link en Bio')
    html_content = html_content.replace('{{IMAGE}}', post['imagen'])
    
    temp_file = f'temp_plan_{index}.html'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    hti = Html2Image(size=(1080, 1920))
    hti.browser.flags = ['--headless', '--disable-gpu', '--hide-scrollbars']
    filename = f'plan_post_{index}.png'
    hti.screenshot(html_file=temp_file, save_as=filename)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
        
    print(f"Generada: {filename}")

if __name__ == "__main__":
    print("Generando las 12 imágenes del plan de publicación...")
    
    # Calcular fechas (1 post cada 2-3 días)
    fecha_base = datetime.date.today()
    
    for i, post in enumerate(PLAN_PUBLICACION, start=1):
        # Avanzamos la fecha para cada post
        fecha_post = fecha_base + datetime.timedelta(days=(i-1)*2)
        fecha_str = fecha_post.strftime("%d/%m/%Y")
        
        crear_imagen(i, post, fecha_str)
        
    print("¡Proceso completado! Revisa los archivos plan_post_1.png hasta plan_post_12.png")
