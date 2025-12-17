VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# -------------------------
# Setup virtual environment
# -------------------------
venv:

	python3 -m venv $(VENV)
	sudo apt update
	sudo apt install portaudio19-dev python3-dev
	$(PIP) install --upgrade pip


# -------------------------
# Install dependencies
# -------------------------
install: venv
	$(PIP) install -r \
		requirements.txt

# -------------------------
# Run listener
# -------------------------
run:
	$(PYTHON) main.py

# -------------------------
# Clean environment
# -------------------------
clean:
	rm -rf $(VENV)

.PHONY: venv install run clean
