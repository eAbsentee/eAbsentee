"""
This script is a scheduled call to the remind web endpoint. That endpoint emails group heads who have had their group code used in the past 24 hours with a reminder email to check the dashboard. You can follow through the code in the admin blueprint.

This script should be scheduled daily.
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# TODO:
# 1) More secure storage of API key
# 2) Post URL's shouldn't be public

params = {'API_KEY': os.environ['API_KEY']}
if os.environ['FLASK_DEBUG'] == 'True':
    requests.post('http://localhost:5000/api/remind/', params=params)
else:
    requests.post('https://www.eabsentee.org/api/remind/', params=params)
