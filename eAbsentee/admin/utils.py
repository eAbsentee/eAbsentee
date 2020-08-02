import os
from ..form.models import User
from dotenv import load_dotenv
load_dotenv()


# 40.3, -75, 6 creates a default zoom over the entire state of Virginia
def get_users(group, date):
    markers = []
    for user in User.query.filter_by(group_code=group).all():
        markers.append({
            'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            'lat': user.lat,
            'lng': user.long,
            'name': user.name
        })
    return markers

def get_groups():
    group_codes = []
    for group in User.query.with_entities(User.group_code).distinct().all():
        group_codes.append(group.group_code)
    return group_codes
