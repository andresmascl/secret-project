# Telegram Bot Controller

Sistema de control de navegador mediante comandos de lenguaje natural enviados a través de Telegram.

## Descripción

Este proyecto permite controlar el navegador Brave en tu PC mediante mensajes de texto enviados a un bot de Telegram. El bot procesa los comandos usando un LLM (Large Language Model) que interpreta el lenguaje natural y los convierte en acciones ejecutables.

## Arquitectura

```
Usuario → Telegram → Bot (PC) → LLM → Bot (PC) → Brave Browser
                         ↑                ↓
                         └─ config.json ──┘
```

### Flujo de Datos

1. **Usuario** envía un mensaje de texto al canal de Telegram
2. **Bot de Telegram** (ejecutándose en PC) detecta el mensaje nuevo
3. **Bot** envía el mensaje al LLM junto con el archivo de configuración local
4. **LLM** procesa la información y genera un comando estructurado
5. **Bot** recibe el comando, lo interpreta y lo ejecuta en Brave Browser

## Estructura del Proyecto

```
telegram-bot-controller/
├── README.md
├── requirements.txt
├── .env.example
├── config/
│   └── config.json          # Configuración de comandos y preferencias
├── src/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── telegram_bot.py      # Manejo del bot de Telegram
│   ├── llm_processor.py     # Comunicación con el LLM
│   ├── browser_controller.py # Control del navegador Brave
│   └── utils/
│       ├── logger.py        # Sistema de logging
│       └── config_loader.py # Carga de configuración
├── logs/
│   └── bot.log              # Logs de ejecución
└── tests/
    ├── test_telegram.py
    ├── test_llm.py
    └── test_browser.py
```

## Requisitos Previos

- Python 3.8 o superior
- Navegador Brave instalado
- Cuenta de Telegram
- Token de bot de Telegram (obtenido de @BotFather)
- Acceso a un servicio LLM (OpenAI, Anthropic, etc.)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/telegram-bot-controller.git
cd telegram-bot-controller
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. Configurar `config/config.json`:
```json
{
  "browser": {
    "path": "/usr/bin/brave-browser",
    "profile": "Default"
  },
  "commands": {
    "open_url": "Abrir navegador en {url}",
    "search": "Buscar {query} en {engine}",
    "close_tab": "Cerrar pestaña actual",
    "new_tab": "Abrir nueva pestaña"
  },
  "llm": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 500
  }
}
```

## Uso

### Iniciar el Bot

```bash
python src/main.py
```

### Ejemplos de Comandos

Envía mensajes al bot de Telegram:

- "Abre YouTube"
- "Busca recetas de pasta en Google"
- "Cierra la pestaña actual"
- "Abre una nueva pestaña con GitHub"
- "Navega a la documentación de Python"

## Configuración

### Variables de Entorno (.env)

```env
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
TELEGRAM_CHAT_ID=tu_chat_id
LLM_API_KEY=tu_api_key_del_llm
LLM_PROVIDER=openai  # o anthropic, etc.
```

### Archivo de Configuración (config.json)

El archivo `config.json` define:

- **browser**: Configuración del navegador Brave
- **commands**: Mapeo de comandos disponibles
- **llm**: Parámetros del modelo de lenguaje
- **preferences**: Preferencias personalizadas del usuario

## Seguridad

- Nunca compartas tu `.env` o tokens en repositorios públicos
- El bot solo responde a chats autorizados (definidos en `TELEGRAM_CHAT_ID`)
- Todos los comandos son validados antes de ejecutarse
- Los logs no contienen información sensible

## Desarrollo

### Ejecutar Tests

```bash
pytest tests/
```

### Agregar Nuevos Comandos

1. Define el comando en `config/config.json`
2. Implementa la lógica en `src/browser_controller.py`
3. Actualiza el prompt del LLM en `src/llm_processor.py`

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Troubleshooting

### El bot no responde
- Verifica que el token de Telegram sea correcto
- Asegúrate de que el bot esté ejecutándose
- Revisa los logs en `logs/bot.log`

### Brave no se abre
- Verifica la ruta del navegador en `config.json`
- Asegúrate de tener permisos de ejecución
- Prueba abriendo Brave manualmente

### El LLM no genera comandos correctos
- Ajusta la temperatura en `config.json`
- Verifica que el prompt sea claro
- Revisa el balance de tu API key

## Licencia

MIT License - Ver archivo `LICENSE` para más detalles

## Autor

Tu Nombre - [@tu_usuario](https://github.com/tu-usuario)

## Agradecimientos

- Python Telegram Bot library
- Selenium WebDriver
- OpenAI / Anthropic API