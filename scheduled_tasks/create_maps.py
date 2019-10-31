from gmplot import gmplot
import googlemaps
import os
import openpyxl
from openpyxl import load_workbook
from datetime import date
# from keys import MAPS_API_KEY

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))

today_date: str = date.today().strftime("%m-%d-%y")
report_path = f'../reports/all_time.xlsx'
report: openpyxl.workbook.Workbook = load_workbook(filename=report_path)
worksheet: openpyxl.worksheet.worksheet.Worksheet = report.active

MAPS_API_KEY = ''

googlemaps_client = googlemaps.Client(key=MAPS_API_KEY)

'''# 40.3, -75, 6 creates a default zoom over the entire state of Virginia '''
gmap_plotter_client = gmplot.GoogleMapPlotter(40.3, -75, 6)

gmap_plotter_client.apikey = MAPS_API_KEY

for cell in worksheet['H']:
    str_value = str(cell.value)
    str_value = str_value.replace('   ', '')
    if '|' in str_value:
        str_value = str_value[0: str_value.find('|')]
    geocode_result = googlemaps_client.geocode(str_value)[0]
    lat, lng = geocode_result['geometry']['location']['lat'], geocode_result['geometry']['location']['lng']
    print(str(lat) + str(lng))
    gmap_plotter_client.marker(lat, lng)

gmap_plotter_client.draw(f'../maps/{today_date}.html')
