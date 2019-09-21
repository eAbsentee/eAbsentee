import hashlib
import yagmail
import os
import openpyxl
import json
from openpyxl import load_workbook
from typing import Dict, List, Tuple
from flask import request, session
import datetime
from datetime import date
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from subprocess import call
from keys import GMAIL_SENDER_ADDRESS, GMAIL_SENDER_PASSWORD, API_KEY

# Change current working directory to directory 'functions.py' is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

form_path: str = 'static/pdf/blankAppFillable.pdf'

packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
can.setFont('Helvetica', 8)
can.drawString(254, 116, 'This application contains an electronic signature.')  # LastName


can.save()
packet.seek(0)
new_pdf = PdfFileReader(packet)
existing_pdf = PdfFileReader(form_path, "rb")
output = PdfFileWriter()
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)

output.write(open('output.pdf', "wb"))
