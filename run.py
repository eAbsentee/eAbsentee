# Imports the create_app method from the eAbsentee package
# Flask recognizes the app exists through scanning for the create_app method
# Run this file using 'flask run' from the CMD line in the root directory 

from eAbsentee.app import create_app

app = create_app()
