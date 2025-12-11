#!/bin/bash
echo "[Scrapbot] Installing virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Done."