"""
Browser Controller - Control del Navegador Brave
================================================

Este módulo controla el navegador Brave mediante Selenium WebDriver:
- Apertura y cierre de pestañas
- Navegación a URLs específicas
- Búsquedas en motores configurados
- Ejecución de scripts JavaScript
- Gestión de sesiones y perfiles

Interpreta los comandos estructurados generados por el LLM y los
ejecuta en el navegador de forma segura y controlada.

Comandos soportados:
    - open_url: Navegar a una URL específica
    - search: Realizar búsquedas en Google, DuckDuckGo, etc.
    - new_tab: Abrir nueva pestaña
    - close_tab: Cerrar pestaña actual
    - go_back: Retroceder en el historial
    - go_forward: Avanzar en el historial

Dependencias:
    - selenium
    - webdriver-manager

Autor: Tu Nombre
Versión: 1.0.0
Fecha: Diciembre 2024
Licencia: MIT
"""