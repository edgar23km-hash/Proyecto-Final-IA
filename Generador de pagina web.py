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

def generar_pagina_web(prompt):
    """
    Toma el prompt del usuario y genera código HTML para una página web simple
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        # Edgar Manuel Quezada Pula 22-EISN-2-054
        # Prompt mejorado para generar código HTML
        system_prompt = """Eres un asistente especializado en generar código HTML para páginas web simples. 
        Genera SOLO el código HTML completo y funcional sin explicaciones adicionales. 
        Incluye CSS embebido en el <style> para que sea visualmente atractivo.
        Asegúrate de que el código sea válido y esté completo con etiquetas html, head y body."""
        
        payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Crea una página web HTML completa y funcional sobre: {prompt}. Incluye CSS embebido."}
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
</html>"""
            # Edgar Manuel Quezada Pula 22-EISN-2-054
            return html_content.strip()
        else:
            error_msg = response_data.get('error', {}).get('message', 'Error desconocido')
            return f"Error en la API: {error_msg}"
            
    except Exception as e:
        return f"Error: {str(e)}"
# Edgar Manuel Quezada Pula 22-EISN-2-054
def generar_html_simple(prompt):
    """
    Genera una página HTML básica sin necesidad de API
    """
    titulo = prompt[:50] + "..." if len(prompt) > 50 else prompt
    
    html_basico = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin: 20px 0;
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 15px;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
        }}
        .content {{
            line-height: 1.8;
            color: #444;
            font-size: 1.1em;
        }}
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .feature {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #007bff;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        .prompt-info {{
            background: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #1890ff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{titulo}</h1>
        
        <div class="prompt-info">
            <strong>Prompt original:</strong> "{prompt}"
        </div>
        
        <div class="content">
            <p>Bienvenido a tu página web generada automaticamente. Esta página fue creada basandose en tu descripcion:</p>
            <p><strong>"{prompt}"</strong></p>
            
            <div class="features">
                <div class="feature">
                    <h3>Diseño Moderno</h3>
                    <p>Interfaz limpia y profesional con gradientes y efectos visuales.</p>
                </div>
                <div class="feature">
                    <h3>Responsive</h3>
                    <p>Se adapta perfectamente a todos los dispositivos y tamaños de pantalla.</p>
                </div>
                <div class="feature">
                    <h3>Rapido</h3>
                    <p>Codigo optimizado para una carga rapida y eficiente.</p>
                </div>
            </div>
            
            <p>Puedes personalizar este codigo HTML segun tus necesidades especificas. Agrega mas secciones, modifica los colores o incluye tus propias imagenes.</p>
        </div>
        
        <div class="footer">
            <p>Pagina generada automaticamente - {titulo}</p>
            <p>Creado con Python y Gradio</p>
        </div>
    </div>
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

def procesar_prompt(mensaje, usar_api=True):
    """
    Función principal que procesa el prompt y genera la página web
    """
    if not mensaje.strip():
        return "Por favor, ingresa un prompt valido", None, None
    
    try:
        # Generar el código HTML
        if usar_api and API_KEY != "tu_api_key_aqui":
            html_code = generar_pagina_web(mensaje)
            fuente = "API"
        else:
            html_code = generar_html_simple(mensaje)
            fuente = "Generador local"
        
        # Si hay error en la generación, usar fallback local
        if html_code.startswith("Error"):
            html_code = generar_html_simple(mensaje)
            fuente = "Generador local (fallback)"
        
        # Crear archivo para descargar
        archivo_html = crear_archivo_html(html_code, mensaje)
        
        # Mensaje de resultado simple
        resultado = f"Pagina web generada exitosamente. Fuente: {fuente}. Tamaño del codigo: {len(html_code)} caracteres."
        
        return resultado, html_code, archivo_html
        
    except Exception as e:
        error_msg = f"Error al procesar el prompt: {str(e)}"
        return error_msg, None, None

# Edgar Manuel Quezada Pula 22-EISN-2-054

# Interfaz de Gradio mejorada con previsualización
with gr.Blocks(theme=gr.themes.Soft()) as iface:
    gr.Markdown("# Generador de Paginas Web con IA")
    gr.Markdown("Describe la pagina web que deseas crear y generaremos el codigo HTML completo para ti. Puedes previsualizar y descargar el resultado inmediatamente.")
    
    with gr.Row():
        with gr.Column(scale=1):
            input_prompt = gr.Textbox(
                label="Describe la pagina web que quieres crear",
                placeholder="Ej: Una pagina de presentacion personal con secciones sobre mis habilidades, experiencia y proyectos...",
                lines=4,
                max_lines=6
            )
            
            btn_generar = gr.Button("Generar Pagina Web", variant="primary", size="lg")
            
            gr.Markdown("Ejemplos rapidos:")
            ejemplos = gr.Examples(
                examples=[
                    ["Pagina de presentacion personal con foto, biografia y enlaces a redes sociales"],
                    ["Landing page para un restaurante con menu, horarios y galeria de fotos"],
                    ["Portafolio para diseñador grafico con galeria de proyectos y formulario de contacto"],
                    ["Blog personal de viajes con articulos, fotos y mapa interactivo"],
                    ["Sitio web para negocio local con servicios, testimonios e informacion de contacto"]
                ],
                inputs=[input_prompt]
            )
            
        with gr.Column(scale=2):
            output_result = gr.Markdown(label="Resultado", value="Esperando tu descripcion...")
            
            with gr.Row():
                btn_descargar = gr.DownloadButton(
                    "Descargar HTML",
                    visible=False,
                    variant="secondary"
                )
            
            html_preview = gr.HTML(
                label="Vista previa de la pagina web",
                value="<div style='padding: 20px; text-align: center; color: #666;'><h3>La previsualizacion aparecera aqui</h3><p>Genera una pagina web para ver la vista previa</p></div>"
            )
    
    # Variables de estado para mantener el archivo temporal
    archivo_temp = gr.State()
    # Edgar Manuel Quezada Pula 22-EISN-2-054
    # Event handlers
    def generar_y_previsualizar(mensaje):
        resultado, html_code, archivo = procesar_prompt(mensaje)
        
        if html_code:
            # Mostrar vista previa
            vista_previa = html_code
            # Mostrar botón de descarga
            return resultado, vista_previa, archivo, gr.DownloadButton(visible=True)
        else:
            return resultado, "<div style='padding: 20px; color: red;'><h3>Error en la generacion</h3><p>No se pudo generar la pagina web.</p></div>", None, gr.DownloadButton(visible=False)
    
    btn_generar.click(
        fn=generar_y_previsualizar,
        inputs=[input_prompt],
        outputs=[output_result, html_preview, archivo_temp, btn_descargar]
    )
    
    # Configurar descarga
    btn_descargar.click(
        fn=lambda x: x,
        inputs=[archivo_temp],
        outputs=[btn_descargar]
    )
# Edgar Manuel Quezada Pula 22-EISN-2-054
if __name__ == "__main__":
    # Verificar si la API key está configurada
    if API_KEY == "tu_api_key_aqui":
        print("ADVERTENCIA: No has configurado tu API_KEY")
        print("La aplicacion usara el generador local")
    
    iface.launch(share=True)