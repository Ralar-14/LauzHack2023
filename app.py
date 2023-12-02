from flask import Flask, render_template, request

import requests
from main import get_token
from mapa import main_fun
import json



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ht.html')

@app.route('/map', methods = ['GET'])
def hello():

    coords_init1 = request.args.get('coords_init_latitude')
    coords_init2 = request.args.get('coords_init_longitude')
    coords_end1 = request.args.get('coords_end_latitude')
    coords_end2 = request.args.get('coords_end_longitude')
    main_coords = main_fun((coords_init1, coords_init2), (coords_end1, coords_end2))
    coords1 = [[float(coords_init1), float(coords_init2)], main_coords[0]]
    coords2 = [[float(coords_end1), float(coords_end2)], main_coords[-1]]

   
    return render_template('index.html', main_coords = main_coords, coords1 = coords1, coords2 = coords2)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)