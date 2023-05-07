# monkey_patch.py
import sys
import PyPDF2 as pypdf

sys.modules["pypdf"] = pypdf
