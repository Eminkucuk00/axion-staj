import sys
import os

# Hugging Face Spaces'in projeyi HAFTA 8 içinden okuyabilmesi için yönlendirici
sys.path.append(os.path.join(os.path.dirname(__file__), "HAFTA 8"))

with open(os.path.join(os.path.dirname(__file__), "HAFTA 8", "dashboard.py"), encoding="utf-8") as f:
    exec(f.read())
