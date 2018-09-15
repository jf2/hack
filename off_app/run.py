import os
import ee

from flask import Flask, render_template
app = Flask(__name__, template_folder='.')
with open('google_maps_api_key.txt') as f:
    app.config['api_key'] = f.read()

ee.Initialize()

@app.route('/')
def hello():
    """Request an image from Earth Engine and render it to a web page."""

    landsat1999 = ee.Image('LANDSAT/LE7_TOA_5YEAR/1999_2003');
    landsat2008 = ee.Image('LANDSAT/LE7_TOA_5YEAR/2008_2012');

    ndvi1999 = landsat1999.select('B4').subtract(landsat1999.select('B3')).divide(landsat1999.select('B4').add(landsat1999.select('B3')));

    mapid = ndvi1999.getMapId({'min': 0, 'max': 1})

    # These could be put directly into template.render, but it
    # helps make the script more readable to pull them out here, especially
    # if this is expanded to include more variables.
    template_values = {
        'mapid': mapid['mapid'],
        'token': mapid['token']
    }

    return render_template('static/html/index.html', **template_values)

if __name__ == '__main__':
    app.run()