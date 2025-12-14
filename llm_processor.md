"""
LLM Processor - Procesamiento de Lenguaje Natural
=================================================

Este módulo gestiona la comunicación con el modelo de lenguaje (LLM) para:
- Interpretar comandos en lenguaje natural
- Generar comandos estructurados ejecutables
- Contextualizar respuestas según la configuración del usuario
- Manejar diferentes proveedores de LLM (OpenAI, Anthropic, etc.)

El LLM actúa como traductor entre el lenguaje natural del usuario y
comandos específicos que el navegador puede ejecutar.

Proveedores soportados:
    - OpenAI (GPT-4, GPT-3.5)
    - Anthropic (Claude)
    - Otros compatibles con API REST

Autor: Tu Nombre
Versión: 1.0.0
Fecha: Diciembre 2024
Licencia: MIT
"""