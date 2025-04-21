from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  

@app.route('/china-map')
def china_map():
    with open('data/regions.json', 'r') as f:
        regions = json.load(f)

    max_progress = len(regions)
    progress = sum(1 for region in regions.values() if region.get("status") is True)

    region_images = {}
    for region_name, data in regions.items():
        demo_dishes = data.get("demo_dishes", [])
        if demo_dishes:
            first_dish = demo_dishes[0].split('(')[0].strip()
            filename = first_dish.lower().replace("'", "").replace(" ", "_") + ".png"
            region_images[region_name] = f"/static/media/{region_name}/{filename}"

    return render_template(
        'china_map.html',
        regions=regions,
        region_images=region_images,
        progress=progress,
        max_progress=max_progress,
        hovered_region=None
    )

@app.route('/learn_culture/<region>', methods=['GET'])
def view_culture(region):
    region_key = region.capitalize()

    with open('data/regions.json', 'r') as f:
        regions = json.load(f)

    return render_template('view_culture.html', region=region_key, regions=regions)

@app.route('/learn_cuisine/<region>', methods=['GET'])
def view_cuisine(region):
    region_key = region.capitalize()

    with open('data/regions.json', 'r') as f:
        regions = json.load(f)

    return render_template('view_cuisine.html', region=region_key, regions=regions)

@app.route('/quiz/<region>', methods=['GET'])
def view_quiz(region):
    region_key = region.capitalize()

    with open('data/regions.json', 'r') as f:
        regions = json.load(f)

    return render_template('view_quiz.html', region=region_key, regions=regions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
