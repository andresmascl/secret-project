# -----------------------------
# Telegram Bot Controller – Makefile
# -----------------------------

VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
CONFIG_DIR := config
ENV_FILE := $(CONFIG_DIR)/.env

# Default target
all: setup

# -----------------------------
# 1. Create virtual environment
# -----------------------------
venv:
	@echo "📦 Creando entorno virtual..."
	python3 -m venv $(VENV)
	@echo "✅ Entorno virtual creado"

# -----------------------------
# 2. Install Python dependencies
# -----------------------------
install: venv
	@echo "📥 Instalando dependencias..."
	. $(VENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt
	@echo "✅ Dependencias instaladas"

# -----------------------------
# 3. Setup configuration files
# -----------------------------
config:
	@echo "⚙️  Configurando archivos..."
	mkdir -p $(CONFIG_DIR)
	@if [ ! -f $(ENV_FILE) ]; then \
		cp $(CONFIG_DIR)/.env.example $(ENV_FILE); \
		echo "📝 Archivo .env creado desde .env.example"; \
		echo "⚠️  IMPORTANTE: Edita $(ENV_FILE) con tus credenciales"; \
	else \
		echo "✅ Archivo .env ya existe"; \
	fi
	@if [ ! -f $(CONFIG_DIR)/config.json ]; then \
		echo "⚠️  config.json no encontrado. Por favor créalo manualmente"; \
	else \
		echo "✅ config.json encontrado"; \
	fi

# -----------------------------
# 4. Validate environment setup
# -----------------------------
validate:
	@echo "🔍 Validando configuración..."
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "❌ Archivo .env no encontrado"; \
		exit 1; \
	fi
	@if [ ! -f $(CONFIG_DIR)/config.json ]; then \
		echo "❌ Archivo config.json no encontrado"; \
		exit 1; \
	fi
	@. $(VENV)/bin/activate && python3 -c "import telegram, selenium, anthropic" 2>/dev/null && \
		echo "✅ Todas las dependencias están instaladas" || \
		(echo "❌ Faltan dependencias. Ejecuta: make install" && exit 1)
	@echo "✅ Configuración validada"

# -----------------------------
# 5. Install browser driver
# -----------------------------
webdriver:
	@echo "🌐 Instalando WebDriver para Brave/Chrome..."
	. $(VENV)/bin/activate && \
	pip install webdriver-manager
	@echo "✅ WebDriver instalado"

# -----------------------------
# 6. Full setup (everything)
# -----------------------------
setup: install config webdriver
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║  ✅ Instalación completada exitosamente                   ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📋 Próximos pasos:"
	@echo "   1. Edita $(ENV_FILE) con tus credenciales"
	@echo "   2. Edita $(CONFIG_DIR)/config.json con tu configuración"
	@echo "   3. Ejecuta 'make validate' para verificar"
	@echo "   4. Ejecuta 'make run' para iniciar el bot"
	@echo ""

# -----------------------------
# 7. Run the bot
# -----------------------------
run: validate
	@echo "🚀 Iniciando Telegram Bot Controller..."
	@echo ""
	. $(VENV)/bin/activate && python3 main.py

.PHONY: clean-venv

# Elimina el entorno virtual
clean-venv:
	rm -rf venv
	@echo "Virtual environment removed."