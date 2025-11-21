# Edgar Manuel Quezada Pula 22-EISN-2-054

import gradio as gr

def responder(mensaje):
    return f"✅ Recibido: {mensaje}"

# Edgar Manuel Quezada Pula 22-EISN-2-054
# generar la interfaz de gradio
iface = gr.Interface(
    fn=responder,
    inputs=gr.Textbox(label="Tu mensaje", placeholder="Escribe aquí..."),
    outputs=gr.Textbox(label="Confirmación"),
    title="Sistema de Mensajes",
    description="Escribe y presiona Enter para enviar"
)

iface.launch()
# Edgar Manuel Quezada Pula 22-EISN-2-054