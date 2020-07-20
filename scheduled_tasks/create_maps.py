from gmplot import gmplot
import googlemaps
import os
import openpyxl
from openpyxl import load_workbook
from datetime import date

today_date: str = date.today().strftime("%m-%d-%y")
googlemaps_client = googlemaps.Client(key=MAPS_API_KEY)

'''# 40.3, -75, 6 creates a default zoom over the entire state of Virginia '''
gmap_plotter_client = gmplot.GoogleMapPlotter(40.3, -75, 6)
gmap_plotter_client.apikey = MAPS_API_KEY

geocode_result = googlemaps_client.geocode(str)[0]
lat, lng = geocode_result['geometry']['location']['lat'], geocode_result['geometry']['location']['lng']
gmap_plotter_client.marker(lat, lng)

gmap_plotter_client.draw(f'../maps/{today_date}.html')
