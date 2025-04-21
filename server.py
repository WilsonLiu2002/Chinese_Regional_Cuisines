from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  

@app.route('/china-map')
def china_map():
    with open('data/region_status.json', 'r') as f:
        region_status = json.load(f)

    with open('data/regions.json', 'r') as f:
        regions = json.load(f)

    max_progress = len(regions)
    progress = sum(1 for status in region_status.values() if status is True)

    return render_template(
        'china_map.html',
        region_status=region_status,
        progress=progress,
        max_progress=max_progress,
        hovered_region=None
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
