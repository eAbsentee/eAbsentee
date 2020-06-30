from flask import request
from subprocess import call
from keys import API_KEY_FCDC
import json
import os
import sys
# Sets CWD to whatever directory app.py is located in
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def add_group(request):
    # call("git pull", shell=True)
    if request.form.get('api_key') != API_KEY_FCDC:
        print('not correct key')
        return

    print('yeet')

    if request.form.get('keycode'):
        with open('static/groups.json') as file:
            groups = json.load(file)
            new_group = {
                request.form.get('keycode'): {
                    "email": request.form.get('group_email')
                }
            }
            groups.update(new_group)
            with open('static/groups.json', 'w') as f:
                json.dump(groups, f, indent=4, sort_keys=True)

    # call("git add .", shell=True)
    # call("git commit -m \"Added new campaign/group\"", shell=True)
    # call("git push origin master", shell=True)
