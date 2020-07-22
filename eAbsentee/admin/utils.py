import os
from gmplot import gmplot
from ..form.models import User
from dotenv import load_dotenv
load_dotenv()


# 40.3, -75, 6 creates a default zoom over the entire state of Virginia
def create_map():
    gmap_plotter_client = gmplot.GoogleMapPlotter(38.2, -79.5, 8)
    gmap_plotter_client.apikey = os.environ["GOOGLE_API_KEY"]

    amt = 0
    for user in User.query.all():
        if amt > 3:
            break
        gmap_plotter_client.marker(float(user.long), float(user.lat))
        amt = amt + 1

    gmap_plotter_client.draw('templates/test.html')
