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
