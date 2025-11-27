# Edgar Manuel Quezada Pula 22-EISN-2-054
import gradio as gr
import requests
import json
import tempfile
import os
from pathlib import Path

# Configura tu API key aquí
API_KEY = "api_key_aquí"
API_URL = "https://api.openai.com/v1/chat/completions"
# Edgar Manuel Quezada Pula 22-EISN-2-054
# Esquemas de colores predefinidos que combinan bien
COLOR_SCHEMES = {
    "Azul y Naranja": {
        "primary": "#2563eb",
        "secondary": "#f59e0b", 
        "accent": "#dc2626",
        "background": "#f8fafc",
        "text": "#1e293b"
    },
    "Verde y Rosa": {
        "primary": "#10b981",
        "secondary": "#ec4899",
        "accent": "#8b5cf6",
        "background": "#f0fdf4",
        "text": "#064e3b"
    },
    "Morado y Amarillo": {
        "primary": "#7c3aed",
        "secondary": "#eab308",
        "accent": "#06b6d4",
        "background": "#faf5ff",
        "text": "#581c87"
    },
    "Rojo y Cian": {
        "primary": "#dc2626",
        "secondary": "#06b6d4",
        "accent": "#16a34a",
        "background": "#fef2f2",
        "text": "#7f1d1d"
    },
    "Oscuro y Dorado": {
        "primary": "#1e293b",
        "secondary": "#d97706",
        "accent": "#7c3aed",
        "background": "#0f172a",
        "text": "#f1f5f9"
    }
}
# Edgar Manuel Quezada Pula 22-EISN-2-054
def generar_pagina_web(prompt, color_scheme):
    """
    Toma el prompt del usuario y genera código HTML para una página web simple
    """
    try:
        colors = COLOR_SCHEMES[color_scheme]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        # Prompt mejorado para generar código HTML con esquema de colores
        system_prompt = f"""Eres un asistente especializado en generar código HTML para páginas web simples. 
        Genera SOLO el código HTML completo y funcional sin explicaciones adicionales. 
        Incluye CSS embebido en el <style> para que sea visualmente atractivo.
        Usa el siguiente esquema de colores:
        - Color primario: {colors['primary']}
        - Color secundario: {colors['secondary']}
        - Color de acento: {colors['accent']}
        - Color de fondo: {colors['background']}
        - Color de texto: {colors['text']}
        
        Asegúrate de que el código sea válido y esté completo con etiquetas html, head y body.
        Incluye iconos de Font Awesome usando CDN."""
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Crea una página web HTML completa y funcional sobre: {prompt}. Incluye CSS embebido y usa el esquema de colores proporcionado."}
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        response = requests.post(API_URL, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            html_content = response_data["choices"][0]["message"]["content"]
            
            # Limpiar el código HTML
            html_content = html_content.strip()
            if '```html' in html_content:
                html_content = html_content.split('```html')[1].split('```')[0]
            elif '```' in html_content:
                html_content = html_content.split('```')[1].split('```')[0]
            
            # Verificar que sea HTML válido
            if not html_content.strip().startswith('<!DOCTYPE html>'):
                if not html_content.strip().startswith('<html>'):
                    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página generada: {prompt}</title>
</head>
<body>
{html_content}
</body>
</html>"""# Edgar Manuel Quezada Pula 22-EISN-2-054
            
            return html_content.strip()
        else:
            error_msg = response_data.get('error', {}).get('message', 'Error desconocido')
            return f"Error en la API: {error_msg}"
            
    except Exception as e:
        return f"Error: {str(e)}"
# Edgar Manuel Quezada Pula 22-EISN-2-054
def generar_html_simple(prompt, color_scheme):
    """
    Genera una página HTML básica sin necesidad de API
    """
    colors = COLOR_SCHEMES[color_scheme]
    titulo = prompt[:50] + "..." if len(prompt) > 50 else prompt
    
    # Determinar si el fondo es oscuro para ajustar colores de texto
    is_dark_bg = color_scheme == "Oscuro y Dorado"
    card_bg = "#1e293b" if is_dark_bg else "white"
    text_color = colors['text']
    secondary_text = "#cbd5e1" if is_dark_bg else "#64748b"
    # Edgar Manuel Quezada Pula 22-EISN-2-054
    html_basico = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {colors['background']};
            color: {text_color};
            line-height: 1.6;
            min-height: 100vh;
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .hero {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="%23ffffff20"><polygon points="1000,100 1000,0 0,100"/></svg>');
            background-size: cover;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .hero h1 {{
            font-size: 3.5em;
            margin-bottom: 20px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .hero p {{
            font-size: 1.3em;
            margin-bottom: 30px;
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        .card {{
            background: {card_bg};
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin: 30px 0;
            border-left: 5px solid {colors['accent']};
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }}
        
        .section-title {{
            color: {colors['primary']};
            font-size: 2.2em;
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: {colors['secondary']};
            border-radius: 2px;
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }}
        
        .feature {{
            background: linear-gradient(135deg, {colors['primary']}15, {colors['secondary']}15);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            border: 2px solid {colors['primary']}30;
            transition: all 0.3s ease;
        }}
        
        .feature:hover {{
            border-color: {colors['primary']};
            transform: scale(1.05);
        }}
        
        .feature-icon {{
            font-size: 3em;
            color: {colors['primary']};
            margin-bottom: 20px;
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .feature h3 {{
            color: {colors['primary']};
            margin-bottom: 15px;
            font-size: 1.4em;
        }}
        
        .feature p {{
            color: {secondary_text};
            line-height: 1.6;
        }}
        
        .prompt-info {{
            background: linear-gradient(135deg, {colors['accent']}15, {colors['primary']}15);
            padding: 25px;
            border-radius: 15px;
            margin: 30px 0;
            border: 2px dashed {colors['accent']}40;
        }}
        
        .color-palette {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        
        .color-item {{
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.8em;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .btn {{
            display: inline-block;
            padding: 15px 30px;
            background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .footer {{
            background: linear-gradient(135deg, {colors['primary']}, {colors['accent']});
            color: white;
            text-align: center;
            padding: 40px 20px;
            margin-top: 60px;
        }}
        
        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 20px 0;
        }}
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        .social-links a {{
            color: white;
            font-size: 1.5em;
            transition: transform 0.3s ease;
        }}
        
        .social-links a:hover {{
            transform: scale(1.2);
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5em;
            }}
            
            .features {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <h1><i class="fas fa-magic"></i> {titulo}</h1>
            <p>Página web generada automáticamente con diseño moderno y colores armoniosos</p>
            <div class="btn">Explorar Más</div>
        </div>
    </section>
# Edgar Manuel Quezada Pula 22-EISN-2-054
    <div class="container">
        <!-- Información del Prompt -->
        <div class="card">
            <h2 class="section-title">Tu Idea Creada</h2>
            <div class="prompt-info">
                <h3><i class="fas fa-lightbulb"></i> Prompt Original:</h3>
                <p>"{prompt}"</p>
            </div>
            
            <!-- Paleta de Colores -->
            <div class="color-palette">
                <div class="color-item" style="background: {colors['primary']}" title="Color Primario">Primario</div>
                <div class="color-item" style="background: {colors['secondary']}" title="Color Secundario">Secundario</div>
                <div class="color-item" style="background: {colors['accent']}" title="Color de Acento">Acento</div>
                <div class="color-item" style="background: {colors['background']}; color: {colors['text']}; border: 2px solid {colors['text']}30" title="Color de Fondo">Fondo</div>
            </div>
        </div>
# Edgar Manuel Quezada Pula 22-EISN-2-054
        <!-- Características -->
        <div class="card">
            <h2 class="section-title">Características Destacadas</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-palette"></i>
                    </div>
                    <h3>Diseño Colorido</h3>
                    <p>Esquema de colores {color_scheme.lower()} cuidadosamente seleccionado para máxima armonía visual y atractivo.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3>Totalmente Responsive</h3>
                    <p>Se adapta perfectamente a todos los dispositivos móviles, tablets y computadoras de escritorio.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h3>Rápido y Moderno</h3>
                    <p>Código optimizado con las últimas tecnologías web para máxima velocidad y performance.</p>
                </div>
                
                <div class="feature">
                    <div class="feature-icon">
                        <i class="fas fa-icons"></i>
                    </div>
                    <h3>Iconos Integrados</h3>
                    <p>Font Awesome integrado para una experiencia visual enriquecida y profesional.</p>
                </div>
            </div>
        </div>
# Edgar Manuel Quezada Pula 22-EISN-2-054
        <!-- Contenido Principal -->
        <div class="card">
            <h2 class="section-title">Sobre Este Proyecto</h2>
            <div class="content">
                <p>Esta página web fue generada automáticamente basándose en tu descripción. El diseño incorpora:</p>
                <ul style="margin: 20px 0; padding-left: 30px;">
                    <li>Esquema de colores <strong>{color_scheme}</strong> armonioso</li>
                    <li>Gradientes y efectos visuales modernos</li>
                    <li>Iconos Font Awesome para mejor experiencia</li>
                    <li>Animaciones suaves y transiciones</li>
                    <li>Diseño completamente responsive</li>
                </ul>
                <p>Puedes personalizar este código HTML según tus necesidades específicas. Agrega más secciones, modifica los colores o incluye tus propias imágenes.</p>
            </div>
        </div>
    </div>
# Edgar Manuel Quezada Pula 22-EISN-2-054
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <h3>¿Te gusta lo que ves?</h3>
            <p>Esta página fue creada automáticamente con Python y Gradio</p>
            
            <div class="social-links">
                <a href="#"><i class="fab fa-facebook"></i></a>
                <a href="#"><i class="fab fa-twitter"></i></a>
                <a href="#"><i class="fab fa-instagram"></i></a>
                <a href="#"><i class="fab fa-linkedin"></i></a>
                <a href="#"><i class="fab fa-github"></i></a>
            </div>
            
            <p style="margin-top: 20px; opacity: 0.8;">
                <small>Generado usando IA - Esquema: {color_scheme}</small>
            </p>
        </div>
    </footer>
</body>
</html>"""
    return html_basico.strip()
# Edgar Manuel Quezada Pula 22-EISN-2-054
def crear_archivo_html(html_content, prompt):
    """Crea un archivo HTML temporal para descargar"""
    # Limpiar el prompt para usarlo como nombre de archivo
    nombre_archivo = "".join(c for c in prompt if c.isalnum() or c in (' ', '-', '_')).rstrip()
    nombre_archivo = nombre_archivo[:30] + ".html" if len(nombre_archivo) > 30 else nombre_archivo + ".html"
    
    # Crear archivo temporal
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
    temp_file.write(html_content)
    temp_file.flush()
    temp_file.close()
    
    return temp_file.name
# Edgar Manuel Quezada Pula 22-EISN-2-054
def procesar_prompt(mensaje, color_scheme, usar_api=True):
    """
    Función principal que procesa el prompt y genera la página web
    """
    if not mensaje.strip():
        return "Por favor, ingresa un prompt valido", None, None
    
    try:
        # Generar el código HTML
        if usar_api and API_KEY != "tu_api_key_aqui":
            html_code = generar_pagina_web(mensaje, color_scheme)
            fuente = "API"
        else:
            html_code = generar_html_simple(mensaje, color_scheme)
            fuente = "Generador local"
        
        # Si hay error en la generación, usar fallback local
        if html_code.startswith("Error"):
            html_code = generar_html_simple(mensaje, color_scheme)
            fuente = "Generador local (fallback)"
        
        # Crear archivo para descargar
        archivo_html = crear_archivo_html(html_code, mensaje)
        
        # Mensaje de resultado simple
        resultado = f"Página web generada exitosamente. \n**Fuente:** {fuente} \n**Esquema de colores:** {color_scheme} \n**Tamaño del código:** {len(html_code)} caracteres"
        
        return resultado, html_code, archivo_html
        
    except Exception as e:
        error_msg = f"Error al procesar el prompt: {str(e)}"
        return error_msg, None, None
# Edgar Manuel Quezada Pula 22-EISN-2-054
# Interfaz de Gradio mejorada con previsualización
with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {max-width: 1200px !important;}") as iface:
    gr.Markdown("""
    # Generador de Páginas Web con IA
    **Crea páginas web hermosas y coloridas con solo describirlas.** 
    Selecciona un esquema de colores y deja que la IA haga el resto.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_prompt = gr.Textbox(
                label=" Describe la página web que quieres crear",
                placeholder="Ej: Una página de presentación personal con secciones sobre mis habilidades, experiencia y proyectos...",
                lines=4,
                max_lines=6
            )
            
            color_scheme = gr.Dropdown(
                label=" Selecciona un esquema de colores",
                choices=list(COLOR_SCHEMES.keys()),
                value="Azul y Naranja",
                info="Colores que combinan perfectamente entre sí"
            )
            
            # Mostrar previsualización de colores
            gr.Markdown("### Muestra de Colores")
            color_preview = gr.HTML("""
            <div style="display: flex; gap: 10px; margin: 15px 0; flex-wrap: wrap;">
                <div style="width: 60px; height: 60px; background: #2563eb; border-radius: 10px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Primario"></div>
                <div style="width: 60px; height: 60px; background: #f59e0b; border-radius: 10px; border: j2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Secundario"></div>
                <div style="width: 60px; height: 60px; background: #dc2626; border-radius: 10px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Acento"></div>
                <div style="width: 60px; height: 60px; background: #f8fafc; border-radius: 10px; border: 2px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Fondo"></div>
            </div>
            """)
            
            btn_generar = gr.Button("Generar Página Web", variant="primary", size="lg")
            # Edgar Manuel Quezada Pula 22-EISN-2-054
            gr.Markdown("###  Ejemplos rápidos")
            ejemplos = gr.Examples(
                examples=[
                    ["Página de presentación personal con foto, biografía y enlaces a redes sociales", "Azul y Naranja"],
                    ["Landing page para un restaurante con menú, horarios y galería de fotos", "Verde y Rosa"],
                    ["Portafolio para diseñador gráfico con galería de proyectos y formulario de contacto", "Morado y Amarillo"],
                    ["Blog personal de viajes con artículos, fotos y mapa interactivo", "Rojo y Cian"],
                    ["Sitio web para negocio local con servicios, testimonios e información de contacto", "Oscuro y Dorado"]
                ],
                inputs=[input_prompt, color_scheme]
            )
            
        with gr.Column(scale=2):
            output_result = gr.Markdown(
                label="Resultado", 
                value="Esperando tu descripción... ¡Se creativo!"
            )
            
            with gr.Row():
                btn_descargar = gr.DownloadButton(
                    "📥 Descargar HTML",
                    visible=False,
                    variant="secondary"
                )
            # Edgar Manuel Quezada Pula 22-EISN-2-054
            html_preview = gr.HTML(
                label="Vista previa de la página web",
value="<div style='padding: 40px; text-align: center; color: #666; background: #161921; border-radius: 15px; border: 2px dashed #ddd;'><h3>La previsualización aparecerá aquí</h3><p>Describe tu página web y selecciona colores para generar una vista previa espectacular</p></div>"            )
    
    # Variables de estado para mantener el archivo temporal
    archivo_temp = gr.State()
    
    # Función para actualizar la previsualización de colores
    def actualizar_color_preview(esquema):
        colors = COLOR_SCHEMES[esquema]
        return f"""
        <div style="display: flex; gap: 10px; margin: 15px 0; flex-wrap: wrap;">
            <div style="width: 60px; height: 60px; background: {colors['primary']}; border-radius: 10px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Primario"></div>
            <div style="width: 60px; height: 60px; background: {colors['secondary']}; border-radius: 10px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Secundario"></div>
            <div style="width: 60px; height: 60px; background: {colors['accent']}; border-radius: 10px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Acento"></div>
            <div style="width: 60px; height: 60px; background: {colors['background']}; border-radius: 10px; border: 2px solid {colors['text']}30; box-shadow: 0 2px 8px rgba(0,0,0,0.2);" title="Fondo"></div>
        </div>
        """
    # Edgar Manuel Quezada Pula 22-EISN-2-054
    # Event handlers
    def generar_y_previsualizar(mensaje, esquema):
        resultado, html_code, archivo = procesar_prompt(mensaje, esquema)
        
        if html_code:
            # Mostrar vista previa
            vista_previa = html_code
            # Mostrar botón de descarga
            return resultado, vista_previa, archivo, gr.DownloadButton(visible=True)
        else:
            return resultado, "<div style='padding: 40px; color: #dc2626; background: #fef2f2; border-radius: 15px; text-align: center;'><h3>Error en la generación</h3><p>No se pudo generar la página web. Intenta con otra descripción.</p></div>", None, gr.DownloadButton(visible=False)
    
    btn_generar.click(
        fn=generar_y_previsualizar,
        inputs=[input_prompt, color_scheme],
        outputs=[output_result, html_preview, archivo_temp, btn_descargar]
    )
    
    color_scheme.change(
        fn=actualizar_color_preview,
        inputs=[color_scheme],
        outputs=[color_preview]
    )
    # Edgar Manuel Quezada Pula 22-EISN-2-054
    # Configurar descarga
    btn_descargar.click(
        fn=lambda x: x,
        inputs=[archivo_temp],
        outputs=[btn_descargar]
    )

if __name__ == "__main__":
    # Verificar si la API key está configurada
    if API_KEY == "tu_api_key_aqui":
        print("ADVERTENCIA: No has configurado tu API_KEY")
        print("La aplicación usará el generador local")
    
    iface.launch(share=True)
    # Edgar Manuel Quezada Pula 22-EISN-2-054