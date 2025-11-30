# Edgar Manuel Quezada Pula 22-EISN-2-054
import gradio as gr
import requests
import json
import tempfile
import os
import base64
from pathlib import Path
import time

# Configura tus API keys aquí
OPENAI_API_KEY = "api_key_aquí"
CHAT_API_URL = "https://api.openai.com/v1/chat/completions"
DALLE_API_URL = "https://api.openai.com/v1/images/generations"
# Edgar Manuel Quezada Pula 22-EISN-2-054
def generar_imagen_dalle(prompt, size="1024x1024", quality="standard"):
    """
    Genera una imagen usando DALL-E 3 basada en el prompt
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": 1
        }
# Edgar Manuel Quezada Pula 22-EISN-2-054
        response = requests.post(DALLE_API_URL, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            image_url = response_data["data"][0]["url"]
            
            # Descargar la imagen y convertir a base64
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                image_base64 = base64.b64encode(img_response.content).decode('utf-8')
                return f"data:image/png;base64,{image_base64}"
            else:
                return None
        else:
            error_msg = response_data.get('error', {}).get('message', 'Error desconocido')
            print(f"Error en DALL-E API: {error_msg}")
            return None
            
    except Exception as e:
        print(f"Error generando imagen: {str(e)}")
        return None
# Edgar Manuel Quezada Pula 22-EISN-2-054
def generar_pagina_web(prompt, color_primario, color_secundario, color_acento, color_fondo, color_texto):
    """
    Toma el prompt del usuario y genera código HTML para una página web simple
    """
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Generar imágenes con DALL-E 3 basadas en el prompt
        imagen_principal = generar_imagen_dalle(
            f"Imagen principal para una página web sobre: {prompt}. "
            f"Estilo moderno, profesional, atractivo visualmente, relacionado con el tema."
        )
        
        imagen_secundaria = generar_imagen_dalle(
            f"Imagen secundaria para complementar una página web sobre: {prompt}. "
            f"Estilo coherente con el tema, visualmente atractiva."
        )
        
        # Usar placeholders si falla la generación de imágenes
        imagen_principal_placeholder = "https://images.unsplash.com/photo-1558655146-364adaf1fcc9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
        imagen_secundaria_placeholder = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
        
        system_prompt = f"""Eres un asistente especializado en generar código HTML para páginas web modernas y estéticas. 
        Genera SOLO el código HTML completo y funcional sin explicaciones adicionales. 
        Incluye CSS embebido en el <style> para que sea visualmente atractivo.
        Usa el siguiente esquema de colores:
        - Color primario: {color_primario}
        - Color secundario: {color_secundario}
        - Color de acento: {color_acento}
        - Color de fondo: {color_fondo}
        - Color de texto: {color_texto}
        
        Asegúrate de que el código sea válido y esté completo con etiquetas html, head y body.
        Incluye Google Fonts (Poppins, Inter, o Montserrat) y iconos de Font Awesome.
        
        IMPORTANTE: 
        1. La página debe tener un sistema de pestañas (tabs) con al menos 4 pestañas diferentes.
        2. Cada pestaña debe contener información diferente relacionada con el tema proporcionado.
        3. Usa diseños modernos con gradientes, sombras y animaciones suaves.
        4. INCLUYE LUGARES PARA IMÁGENES GENERADAS CON IA en las siguientes ubicaciones:
           - Una imagen principal en el header/hero section
           - Imágenes en las diferentes pestañas relacionadas con el contenido
        5. Usa las siguientes URLs para las imágenes (reemplázalas en el código):
           IMAGEN_PRINCIPAL: {imagen_principal or imagen_principal_placeholder}
           IMAGEN_SECUNDARIA: {imagen_secundaria or imagen_secundaria_placeholder}
        
        El tema principal es: {prompt}"""
# Edgar Manuel Quezada Pula 22-EISN-2-054
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Crea una página web HTML completa y funcional sobre: {prompt}. Incluye CSS embebido y usa el esquema de colores proporcionado. La página debe tener un sistema de pestañas con al menos 4 pestañas diferentes, cada una con contenido único y botones para navegar. Usa fuentes modernas de Google Fonts y diseños atractivos. INCLUYE ESPACIOS PARA IMÁGENES en el header y en las diferentes secciones."}
            ],
            "max_tokens": 3000,
            "temperature": 0.7
        }

        response = requests.post(CHAT_API_URL, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            html_content = response_data["choices"][0]["message"]["content"]
            
            # Limpiar el código HTML
            html_content = html_content.strip()
            if '```html' in html_content:
                html_content = html_content.split('```html')[1].split('```')[0]
            elif '```' in html_content:
                html_content = html_content.split('```')[1].split('```')[0]
            
            # Reemplazar placeholders con imágenes reales si están disponibles
            if imagen_principal:
                html_content = html_content.replace("IMAGEN_PRINCIPAL", imagen_principal)
            else:
                html_content = html_content.replace("IMAGEN_PRINCIPAL", imagen_principal_placeholder)
                
            if imagen_secundaria:
                html_content = html_content.replace("IMAGEN_SECUNDARIA", imagen_secundaria)
            else:
                html_content = html_content.replace("IMAGEN_SECUNDARIA", imagen_secundaria_placeholder)
            
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
            
            return html_content.strip()
        else:
            error_msg = response_data.get('error', {}).get('message', 'Error desconocido')
            return f"Error en la API: {error_msg}"
            
    except Exception as e:
        return f"Error: {str(e)}"
# Edgar Manuel Quezada Pula 22-EISN-2-054
def generar_html_simple(prompt, color_primario, color_secundario, color_acento, color_fondo, color_texto):
    """
    Genera una página HTML básica con pestañas sin necesidad de API
    """
    titulo = prompt[:50] + "..." if len(prompt) > 50 else prompt
    
    # Generar imágenes con DALL-E 3
    imagen_principal = generar_imagen_dalle(
        f"Imagen principal para una página web sobre: {prompt}. "
        f"Estilo moderno, profesional, atractivo visualmente."
    )
    
    imagen_galeria1 = generar_imagen_dalle(
        f"Imagen relacionada con: {prompt}. Estilo coherente, visualmente atractiva."
    )
    
    imagen_galeria2 = generar_imagen_dalle(
        f"Otra imagen relacionada con: {prompt}. Estilo coherente."
    )
    # Edgar Manuel Quezada Pula 22-EISN-2-054
    # Usar placeholders si falla la generación de imágenes
    imagen_principal = imagen_principal or "https://images.unsplash.com/photo-1558655146-364adaf1fcc9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    imagen_galeria1 = imagen_galeria1 or "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    imagen_galeria2 = imagen_galeria2 or "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80"
    
    # Determinar si el fondo es oscuro para ajustar colores de texto
    def is_dark_color(hex_color):
        # Convertir hex a RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        # Calcular luminosidad
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    
    is_dark_bg = is_dark_color(color_fondo)
    card_bg = "rgba(255, 255, 255, 0.95)" if is_dark_bg else "rgba(255, 255, 255, 0.95)"
    secondary_text = "#e2e8f0" if is_dark_bg else "#64748b"
# Edgar Manuel Quezada Pula 22-EISN-2-054
    html_basico = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: {color_primario};
            --secondary: {color_secundario};
            --accent: {color_acento};
            --background: {color_fondo};
            --text: {color_texto};
            --card-bg: {card_bg};
            --shadow: 0 20px 40px rgba(0,0,0,0.1);
            --shadow-hover: 0 30px 60px rgba(0,0,0,0.15);
        }}
        
        body {{
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--background);
            color: var(--text);
            line-height: 1.7;
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 10% 20%, {color_primario}15 0%, transparent 20%),
                radial-gradient(circle at 90% 80%, {color_secundario}15 0%, transparent 20%);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        
        /* Header Moderno con Imagen */
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 80px 20px;
            text-align: center;
            border-radius: 0 0 40px 40px;
            margin-bottom: 60px;
            box-shadow: var(--shadow);
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('{imagen_principal}') center/cover;
            opacity: 0.2;
        }}
        
        .header-content {{
            position: relative;
            z-index: 2;
        }}
        
        .header h1 {{
            font-family: 'Poppins', sans-serif;
            font-size: 3.5em;
            margin-bottom: 20px;
            font-weight: 800;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header p {{
            font-size: 1.3em;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto 30px;
            font-weight: 300;
        }}
        
        .header-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 50px;
            font-size: 0.9em;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        /* Sistema de Pestañas Mejorado */
        .tabs-system {{
            background: var(--card-bg);
            border-radius: 25px;
            box-shadow: var(--shadow);
            overflow: hidden;
            margin-bottom: 60px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .tabs-header {{
            display: flex;
            background: linear-gradient(135deg, var(--primary)10, var(--secondary)10);
            border-bottom: 2px solid var(--primary)20;
            flex-wrap: wrap;
            backdrop-filter: blur(10px);
        }}
        
        .tab-btn {{
            flex: 1;
            min-width: 160px;
            padding: 25px 20px;
            background: transparent;
            border: none;
            cursor: pointer;
            font-family: 'Poppins', sans-serif;
            font-size: 1.1em;
            font-weight: 600;
            color: var(--primary);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            overflow: hidden;
        }}
        
        .tab-btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
            transition: left 0.6s;
        }}
        
        .tab-btn:hover::before {{
            left: 100%;
        }}
        
        .tab-btn:hover {{
            background: var(--primary)15;
            color: var(--primary);
            transform: translateY(-2px);
        }}
        
        .tab-btn.active {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            box-shadow: 0 8px 25px var(--primary)40;
            transform: translateY(0);
        }}
        
        .tab-btn.active::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100%;
            height: 3px;
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent);
        }}
        
        .tab-icon {{
            font-size: 1.3em;
            transition: transform 0.3s ease;
        }}
        
        .tab-btn:hover .tab-icon {{
            transform: scale(1.2) rotate(5deg);
        }}
        
        .tab-content {{
            display: none;
            padding: 50px;
            animation: fadeInUp 0.6s ease;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeInUp {{
            from {{ 
                opacity: 0; 
                transform: translateY(20px); 
            }}
            to {{ 
                opacity: 1; 
                transform: translateY(0); 
            }}
        }}
        
        .tab-content h2 {{
            font-family: 'Poppins', sans-serif;
            color: var(--primary);
            margin-bottom: 30px;
            font-size: 2.5em;
            font-weight: 700;
            position: relative;
            padding-bottom: 15px;
        }}
        
        .tab-content h2::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 80px;
            height: 4px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 2px;
        }}
        
        .tab-content h3 {{
            font-family: 'Poppins', sans-serif;
            color: var(--secondary);
            margin: 30px 0 20px 0;
            font-size: 1.6em;
            font-weight: 600;
        }}
        
        .tab-content p {{
            margin-bottom: 25px;
            line-height: 1.8;
            font-size: 1.15em;
            color: var(--text);
            font-weight: 400;
        }}
        
        .tab-content ul, .tab-content ol {{
            margin: 25px 0;
            padding-left: 35px;
        }}
        
        .tab-content li {{
            margin-bottom: 15px;
            line-height: 1.7;
            font-size: 1.1em;
            position: relative;
        }}
        
        .tab-content li::before {{
            content: '▸';
            color: var(--accent);
            font-weight: bold;
            position: absolute;
            left: -20px;
        }}
        
        .content-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 35px;
            margin: 40px 0;
        }}
        
        .content-card {{
            background: linear-gradient(135deg, var(--primary)08, var(--secondary)08);
            padding: 35px 30px;
            border-radius: 20px;
            border-left: 5px solid var(--accent);
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .content-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, var(--primary), var(--accent));
        }}
        
        .content-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: var(--shadow-hover);
        }}
        
        .content-card h4 {{
            font-family: 'Poppins', sans-serif;
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 1.4em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        .card-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.3em;
        }}
        
        .feature-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin: 35px 0;
        }}
        
        .feature-item {{
            background: linear-gradient(135deg, var(--primary)10, var(--secondary)10);
            padding: 30px 25px;
            border-radius: 18px;
            border: 1px solid var(--primary)20;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        
        .feature-item:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow);
            border-color: var(--primary)40;
        }}
        
        .feature-icon {{
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            color: white;
            font-size: 2em;
            box-shadow: 0 10px 25px var(--primary)30;
        }}
        
        .feature-item h4 {{
            color: var(--primary);
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: 600;
        }}
        
        .stats-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            margin: 40px 0;
        }}
        
        .stat-item {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            padding: 35px 25px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 15px 35px var(--primary)40;
            transition: transform 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-item::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s;
        }}
        
        .stat-item:hover::before {{
            transform: rotate(45deg) translate(50%, 50%);
        }}
        
        .stat-item:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 3em;
            font-weight: 800;
            margin-bottom: 10px;
            font-family: 'Poppins', sans-serif;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
            margin: 35px 0;
        }}
        
        .gallery-item {{
            background: linear-gradient(135deg, var(--primary)15, var(--secondary)15);
            height: 180px;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            font-weight: 600;
            font-size: 1.3em;
            transition: all 0.3s ease;
            border: 2px dashed var(--primary)30;
            position: relative;
            overflow: hidden;
        }}
        
        .gallery-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .gallery-item:hover img {{
            transform: scale(1.1);
        }}
        
        .gallery-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--primary)20, var(--secondary)20);
            z-index: 1;
        }}
        
        .gallery-item span {{
            position: relative;
            z-index: 2;
        }}
        
        .gallery-item:hover {{
            transform: scale(1.05);
            border-color: var(--primary);
            box-shadow: 0 10px 25px var(--primary)20;
        }}
        
        .image-section {{
            margin: 40px 0;
            text-align: center;
        }}
        
        .main-image {{
            width: 100%;
            max-width: 800px;
            height: 400px;
            border-radius: 20px;
            object-fit: cover;
            box-shadow: var(--shadow);
            margin: 20px auto;
            display: block;
            border: 5px solid white;
        }}
        
        .image-caption {{
            font-style: italic;
            color: var(--secondary);
            margin-top: 10px;
            font-size: 1.1em;
        }}
        
        .footer {{
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: white;
            text-align: center;
            padding: 60px 20px;
            border-radius: 40px 40px 0 0;
            margin-top: 80px;
            position: relative;
            overflow: hidden;
        }}
        
        .footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" fill="%23ffffff10"><polygon points="1000,100 1000,0 0,100"/></svg>');
            background-size: cover;
        }}
        
        .footer-content {{
            position: relative;
            z-index: 2;
        }}
        
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 16px 35px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.6s;
        }}
        
        .btn:hover::before {{
            left: 100%;
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        }}
        
        .highlight {{
            background: linear-gradient(135deg, var(--accent)15, var(--primary)15);
            padding: 35px 30px;
            border-radius: 20px;
            border-left: 5px solid var(--accent);
            margin: 35px 0;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .highlight::before {{
            content: '';
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 2em;
            opacity: 0.3;
        }}
        
        .social-links {{
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }}
        
        .social-link {{
            width: 50px;
            height: 50px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-decoration: none;
            font-size: 1.3em;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
        }}
        
        .social-link:hover {{
            background: white;
            color: var(--primary);
            transform: translateY(-3px) scale(1.1);
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2.5em;
            }}
            
            .header {{
                padding: 60px 20px;
            }}
            
            .tabs-header {{
                flex-direction: column;
            }}
            
            .tab-btn {{
                min-width: 100%;
                padding: 20px;
            }}
            
            .tab-content {{
                padding: 30px 20px;
            }}
            
            .content-grid {{
                grid-template-columns: 1fr;
                gap: 25px;
            }}
            
            .stats-container {{
                grid-template-columns: 1fr;
            }}
            
            .main-image {{
                height: 250px;
            }}
        }}
        
        /* Animaciones adicionales */
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .floating {{
            animation: float 3s ease-in-out infinite;
        }}
        
        .ai-badge {{
            background: linear-gradient(135deg, var(--accent), var(--primary));
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <!-- Header Moderno con Imagen de Fondo -->
    <div class="header">
        <div class="header-content">
            <h1><i class="fas fa-star floating"></i> {titulo}</h1>
            <p>Descubre un mundo de posibilidades con nuestro diseño moderno y sistema de pestañas intuitivo</p>
        </div>
    </div>
    
    <div class="container">
        <!-- Sistema de Pestañas Mejorado -->
        <div class="tabs-system">
            <!-- Botones de Pestañas -->
            <div class="tabs-header">
                <button class="tab-btn active" onclick="openTab('tab1')">
                    <span class="tab-icon"><i class="fas fa-home"></i></span>
                    Inicio
                </button>
                <button class="tab-btn" onclick="openTab('tab2')">
                    <span class="tab-icon"><i class="fas fa-info-circle"></i></span>
                    Información
                </button>
                <button class="tab-btn" onclick="openTab('tab3')">
                    <span class="tab-icon"><i class="fas fa-cogs"></i></span>
                    Características
                </button>
                <button class="tab-btn" onclick="openTab('tab4')">
                    <span class="tab-icon"><i class="fas fa-images"></i></span>
                    Galería
                </button>
                <button class="tab-btn" onclick="openTab('tab5')">
                    <span class="tab-icon"><i class="fas fa-envelope"></i></span>
                    Contacto
                </button>
            </div>
            
            <!-- Contenido de Pestañas -->
            <div id="tab1" class="tab-content active">
                <h2>Bienvenido a {titulo}</h2>
                <p>Explora una experiencia web excepcional diseñada con las últimas tendencias en diseño y tecnología. Navega a través de nuestras pestañas para descubrir contenido único y funcionalidades innovadoras.</p>
                
                <div class="image-section">
                    <img src="{imagen_principal}" alt="Imagen principal generada con IA" class="main-image">
                    <p class="image-caption">Imagen generada con inteligencia artificial específicamente para este tema</p>
                </div>
                
                <div class="highlight">
                    <h3><i class="fas fa-gem"></i> Característica Destacada</h3>
                    <p>Nuestro sistema de pestañas avanzado te ofrece una navegación fluida y elegante, combinando estética moderna con máxima funcionalidad. Todas las imágenes han sido generadas con DALL-E 3 específicamente para este contenido.</p>
                </div>
                
                <div class="content-grid">
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-bolt"></i></span>
                            Ultra Rápido
                        </h4>
                        <p>Diseño optimizado para máxima velocidad de carga y experiencia de usuario excepcional.</p>
                    </div>
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-mobile-alt"></i></span>
                            Totalmente Responsive
                        </h4>
                        <p>Adaptación perfecta a todos los dispositivos, desde móviles hasta pantallas de escritorio.</p>
                    </div>
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-robot"></i></span>
                            IA Integrada
                        </h4>
                        <p>Imágenes generadas con DALL-E 3 específicamente para tu contenido.</p>
                    </div>
                </div>
            </div>
            
            <div id="tab2" class="tab-content">
                <h2>Información Detallada</h2>
                <p>Sumérgete en los detalles y descubre todo lo que necesitas saber sobre nuestra plataforma y servicios.</p>
                
                <div class="image-section">
                    <img src="{imagen_galeria1}" alt="Imagen informativa generada con IA" class="main-image">
                    <p class="image-caption">Visualización única creada con inteligencia artificial</p>
                </div>
                
                <h3><i class="fas fa-rocket"></i> Acerca de Nosotros</h3>
                <p>Somos especialistas en crear experiencias digitales memorables que combinan diseño innovador con tecnología de vanguardia, incluyendo generación de imágenes con IA.</p>
                
                <div class="stats-container">
                    <div class="stat-item">
                        <div class="stat-number">98%</div>
                        <div>Satisfacción del Cliente</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">24/7</div>
                        <div>Soporte Disponible</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">150+</div>
                        <div>Proyectos Exitosos</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">5★</div>
                        <div>Calificación Promedio</div>
                    </div>
                </div>
                
                <h3><i class="fas fa-bullseye"></i> Nuestra Misión</h3>
                <p>Transformar ideas en experiencias digitales extraordinarias que inspiren, conecten y generen impacto positivo, utilizando las tecnologías más avanzadas como la inteligencia artificial.</p>
            </div>
            
            <div id="tab3" class="tab-content">
                <h2>Características Principales</h2>
                <p>Descubre el conjunto completo de funcionalidades que hacen de nuestra plataforma la elección perfecta.</p>
                
                <div class="feature-list">
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h4>Seguridad Avanzada</h4>
                        <p>Protección enterprise-level con encriptación de última generación</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-tachometer-alt"></i>
                        </div>
                        <h4>Alto Rendimiento</h4>
                        <p>Optimización extrema para velocidad y eficiencia incomparables</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <h4>IA Integrada</h4>
                        <p>Generación automática de imágenes con DALL-E 3 para cada proyecto</p>
                    </div>
                    <div class="feature-item">
                        <div class="feature-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <h4>Colaboración en Tiempo Real</h4>
                        <p>Trabajo en equipo fluido con sincronización instantánea</p>
                    </div>
            </div>
            
            <div id="tab4" class="tab-content">
                <h2>Galería de Imágenes IA</h2>
                <p>Explora nuestra galería de imágenes generadas con inteligencia artificial específicamente para este proyecto.</p>
                
                <div class="gallery">
                    <div class="gallery-item">
                        <img src="{imagen_principal}" alt="Imagen IA 1">
                        <span>Imagen Principal</span>
                    </div>
                    <div class="gallery-item">
                        <img src="{imagen_galeria1}" alt="Imagen IA 2">
                        <span>Visualización 1</span>
                    </div>
                    <div class="gallery-item">
                        <img src="{imagen_galeria2}" alt="Imagen IA 3">
                        <span>Visualización 2</span>
                    </div>
                    <div class="gallery-item" style="background: linear-gradient(135deg, var(--primary), var(--secondary));">
                        <span>+ Más Imágenes</span>
                    </div>
                </div>
                
                <div class="highlight">
                    <h3><i class="fas fa-robot"></i> Tecnología DALL-E 3</h3>
                    <p>Todas las imágenes en esta página han sido generadas automáticamente usando DALL-E 3, el modelo de generación de imágenes más avanzado de OpenAI. Cada imagen es única y creada específicamente para el tema: "{prompt}"</p>
                </div>
                
                <h3><i class="fas fa-trophy"></i> Proyectos Destacados</h3>
                <div class="content-grid">
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-project-diagram"></i></span>
                            E-commerce Elite
                        </h4>
                        <p>Plataforma de comercio electrónico con inteligencia artificial integrada.</p>
                        <button class="btn" style="margin-top: 20px;">
                            <i class="fas fa-external-link-alt"></i> Ver Proyecto
                        </button>
                    </div>
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-mobile"></i></span>
                            App Móvil Pro
                        </h4>
                        <p>Aplicación nativa multiplataforma con realidad aumentada.</p>
                        <button class="btn" style="margin-top: 20px;">
                            <i class="fas fa-external-link-alt"></i> Ver Proyecto
                        </button>
                    </div>
                </div>
            </div>
            
            <div id="tab5" class="tab-content">
                <h2>Contacto y Soporte</h2>
                <p>Estamos aquí para ayudarte. Contáctanos a través de cualquiera de nuestros canales disponibles.</p>
                
                <div class="image-section">
                    <img src="{imagen_galeria2}" alt="Imagen de contacto generada con IA" class="main-image">
                    <p class="image-caption">Conectando ideas con tecnología avanzada</p>
                </div>
                
                <div class="content-grid">
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-envelope"></i></span>
                            Correo Electrónico
                        </h4>
                        <p>info{chr(64)}ejemplo.com</p>
                        <p>soporte{chr(64)}ejemplo.com</p>
                    </div>
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-phone"></i></span>
                            Teléfono
                        </h4>
                        <p>+1 (555) 123-4567</p>
                        <p>+1 (555) 987-6543</p>
                    </div>
                    <div class="content-card">
                        <h4>
                            <span class="card-icon"><i class="fas fa-map-marker-alt"></i></span>
                            Oficina Central
                        </h4>
                        <p>123 Innovation Drive</p>
                        <p>Tech City, Digital State 12345</p>
                    </div>
                </div>
                
                <h3><i class="fas fa-clock"></i> Horario de Atención</h3>
                <div class="feature-list">
                    <div class="feature-item">
                        <h4><i class="fas fa-calendar-week"></i> Lunes - Viernes</h4>
                        <p>9:00 AM - 6:00 PM</p>
                    </div>
                    <div class="feature-item">
                        <h4><i class="fas fa-calendar-day"></i> Sábados</h4>
                        <p>10:00 AM - 2:00 PM</p>
                    </div>
                    <div class="feature-item">
                        <h4><i class="fas fa-calendar-times"></i> Domingos</h4>
                        <p>Descanso creativo</p>
                    </div>
                </div>
                
                <div class="highlight">
                    <h3><i class="fas fa-robot"></i> Soporte con IA</h3>
                    <p>Nuestro sistema de soporte integra inteligencia artificial para respuestas más rápidas y precisas. Además, podemos generar imágenes personalizadas con DALL-E 3 para tus proyectos en tiempo real.</p>
                    <button class="btn" style="margin-top: 20px;">
                        <i class="fas fa-star"></i> Solicitar Demo IA
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Footer Mejorado -->
    <div class="footer">
        <div class="footer-content">
            <h3 style="font-family: 'Poppins', sans-serif; font-size: 2.2em; margin-bottom: 20px;">
                ¿Listo para comenzar tu proyecto?
            </h3>
            <p style="font-size: 1.2em; margin-bottom: 30px; opacity: 0.9;">
                Transformemos tus ideas en una experiencia digital extraordinaria con IA
            </p>
            
            <div class="social-links">
                <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                <a href="#" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                <a href="#" class="social-link"><i class="fab fa-github"></i></a>
            </div>
            
            <p style="margin-top: 40px; opacity: 0.8; font-size: 0.9em;">
                <small>© 2024 {titulo}. Todos los derechos reservados.</small>
            </p>
        </div>
    </div>
    
    <script>
        function openTab(tabId) {{
            // Ocultar todos los contenidos de pestañas
            var tabContents = document.getElementsByClassName('tab-content');
            for (var i = 0; i < tabContents.length; i++) {{
                tabContents[i].classList.remove('active');
            }}
            
            // Desactivar todos los botones de pestañas
            var tabButtons = document.getElementsByClassName('tab-btn');
            for (var i = 0; i < tabButtons.length; i++) {{
                tabButtons[i].classList.remove('active');
            }}
            
            // Mostrar la pestaña actual y activar el botón
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }}
        
        // Efectos de scroll suave
        document.addEventListener('DOMContentLoaded', function() {{
            openTab('tab1');
            
            // Añadir efecto de aparición gradual a los elementos
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};
            
            const observer = new IntersectionObserver(function(entries) {{
                entries.forEach(function(entry) {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);
            
            // Observar elementos para animación
            const animatedElements = document.querySelectorAll('.content-card, .feature-item, .stat-item, .gallery-item');
            animatedElements.forEach(function(el) {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            }});
        }});
    </script>
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
def procesar_prompt(mensaje, color_primario, color_secundario, color_acento, color_fondo, color_texto, usar_api=True):
    """
    Función principal que procesa el prompt y genera la página web
    """
    if not mensaje.strip():
        return "Por favor, ingresa un prompt valido", None, None
    
    try:
        # Generar el código HTML
        if usar_api and OPENAI_API_KEY != "tu_api_key_aqui":
            html_code = generar_pagina_web(mensaje, color_primario, color_secundario, color_acento, color_fondo, color_texto)
            fuente = "API"
        else:
            html_code = generar_html_simple(mensaje, color_primario, color_secundario, color_acento, color_fondo, color_texto)
            fuente = "Generador local"
        
        # Si hay error en la generación, usar fallback local
        if html_code.startswith("Error"):
            html_code = generar_html_simple(mensaje, color_primario, color_secundario, color_acento, color_fondo, color_texto)
            fuente = "Generador local (fallback)"
        
        # Crear archivo para descargar
        archivo_html = crear_archivo_html(html_code, mensaje)
        
        # Mensaje de resultado
        resultado = f"""## Página web generada exitosamente

¡Tu página web ahora incluye imágenes únicas generadas específicamente para tu tema!"""

        return resultado, html_code, archivo_html
        
    except Exception as e:
        error_msg = f"Error al procesar el prompt: {str(e)}"
        return error_msg, None, None
# Edgar Manuel Quezada Pula 22-EISN-2-054
# Interfaz de Gradio mejorada
with gr.Blocks(theme=gr.themes.Soft(), css=".gradio-container {max-width: 1200px !important;}") as iface:
    gr.Markdown("""
    # Generador de Páginas Web
    
    *Describe tu página y selecciona colores para crear tu página.*
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            input_prompt = gr.Textbox(
                label="Describe la página web que quieres crear",
                placeholder="Ej: Una página de presentación personal con secciones sobre mis habilidades, experiencia y proyectos...",
                lines=4,
                max_lines=6
            )
            
            gr.Markdown("Personaliza los Colores")
            
            with gr.Row():
                color_primario = gr.ColorPicker(
                    label="Color Primario",
                    value="#6366f1",
                    info="Color principal para encabezados y elementos destacados"
                )
                color_secundario = gr.ColorPicker(
                    label="Color Secundario", 
                    value="#f59e0b",
                    info="Color para botones y elementos secundarios"
                )
            
            with gr.Row():
                color_acento = gr.ColorPicker(
                    label="Color de Acento",
                    value="#ec4899", 
                    info="Color para detalles y elementos de énfasis"
                )
                color_fondo = gr.ColorPicker(
                    label="Color de Fondo",
                    value="#f8fafc",
                    info="Color de fondo general de la página"
                )
            
            color_texto = gr.ColorPicker(
                label="Color de Texto",
                value="#1e293b",
                info="Color principal para el texto"
            )
            
            btn_generar = gr.Button("Generar Página Web con IA", variant="primary", size="lg")
            
            gr.Markdown("### Ejemplos rápidos")
            ejemplos = gr.Examples(
                examples=[
                    ["Página de presentación personal con foto, biografía y enlaces a redes sociales"],
                    ["Landing page para un restaurante con menú, horarios y galería de fotos"],
                    ["Portafolio para diseñador gráfico con galería de proyectos y formulario de contacto"],
                    ["Blog personal de viajes con artículos, fotos y mapa interactivo"],
                    ["Sitio web para negocio local con servicios, testimonios e información de contacto"]
                ],
                inputs=[input_prompt]
            )
            
        with gr.Column(scale=2):
            output_result = gr.Markdown(
                label="Resultado"
            )
            
            with gr.Row():
                btn_descargar = gr.DownloadButton(
                    "Descargar HTML",
                    visible=False,
                    variant="secondary"
                )
            
            html_preview = gr.HTML(
                label="Vista previa de la página web",
                value="""<div style='padding: 60px 40px; text-align: center; color: #666; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); border-radius: 20px; border: 2px dashed #cbd5e1;'>
                    <div style='font-size: 4em; margin-bottom: 20px;'></div>
                    <h3 style='color: #334155; margin-bottom: 15px; font-family: "Poppins", sans-serif;'>¡Generación con IA Activada!</h3>
                    <p style='font-size: 1.1em; color: #64748b;'>Describe tu página web y selecciona colores para generar una vista previa con:</p>
                    <ul style='text-align: left; display: inline-block; margin: 20px 0; color: #64748b;'>
                    </ul>
                </div>"""
            )
    
    # Variables de estado para mantener el archivo temporal
    archivo_temp = gr.State()
    
    # Event handlers
    def generar_y_previsualizar(mensaje, primario, secundario, acento, fondo, texto):
        resultado, html_code, archivo = procesar_prompt(mensaje, primario, secundario, acento, fondo, texto)
        
        if html_code:
            # Mostrar vista previa
            vista_previa = html_code
            # Mostrar botón de descarga
            return resultado, vista_previa, archivo, gr.DownloadButton(visible=True)
        else:
            return resultado, """<div style='padding: 60px 40px; color: #dc2626; background: #fef2f2; border-radius: 20px; text-align: center; border: 2px solid #fecaca;'>
                <div style='font-size: 4em; margin-bottom: 20px;'>X</div>
                <h3 style='color: #dc2626; margin-bottom: 15px; font-family: "Poppins", sans-serif;'>Error en la generación</h3>
                <p style='font-size: 1.1em; color: #b91c1c;'>No se pudo generar la página web. Intenta con otra descripción.</p>
            </div>""", None, gr.DownloadButton(visible=False)
    
    btn_generar.click(
        fn=generar_y_previsualizar,
        inputs=[input_prompt, color_primario, color_secundario, color_acento, color_fondo, color_texto],
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
    if OPENAI_API_KEY == "tu_api_key_aqui":
        print("ADVERTENCIA: No has configurado tu OPENAI_API_KEY")
        print("La aplicación usará el generador local")
    
    iface.launch(share=True)
    # Edgar Manuel Quezada Pula 22-EISN-2-054