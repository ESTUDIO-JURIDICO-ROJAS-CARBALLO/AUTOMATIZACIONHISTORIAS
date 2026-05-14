import os
import datetime
from html2image import Html2Image

def crear_imagen_ruidos():
    with open('story_template.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    html_tit = "<span>RUIDOS MOLESTOS</span><br>RESPONSABILIDAD LEGAL"
    
    subtitulo = "Un club de pádel en Río Cuarto fue obligado a cerrar hasta reducir el ruido.<br><br>Los vecinos tienen derechos. Conocé los tuyos. ⚖️<br><br>Consultá con Rojas & Carballo 📲"
    
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    fuente_fecha = f"{fecha} • CASO RÍO CUARTO"
    
    # Imagen de cancha de tenis / pádel de Unsplash
    imagen_padel = "https://images.unsplash.com/photo-1622279457486-62dcc4a631d6?w=800&q=80" 
    
    html_content = html_content.replace('{{TITLE}}', html_tit)
    html_content = html_content.replace('{{SUBTITLE}}', subtitulo)
    html_content = html_content.replace('{{SOURCE}}', fuente_fecha.upper())
    html_content = html_content.replace('{{LINK}}', 'Link en Bio')
    html_content = html_content.replace('{{IMAGE}}', imagen_padel)
    
    temp_file = 'temp_ruidos.html'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    hti = Html2Image(size=(1080, 1920))
    hti.browser.flags = ['--headless', '--disable-gpu', '--hide-scrollbars']
    filename = 'historia_ruidos.png'
    hti.screenshot(html_file=temp_file, save_as=filename)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
        
    print(f"Generada exitosamente: {filename}")

if __name__ == "__main__":
    crear_imagen_ruidos()
