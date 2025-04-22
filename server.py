from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
from utils import data_loader

app = Flask(__name__)

@app.context_processor
def inject_regions():
    # This makes `regions` available in ALL templates
    return dict(regions=data_loader.load_all_regions())

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

    # load this region’s quiz
    quiz = data_loader.get_quiz_for_region(region_key)
    feedback = data_loader.load_feedback()

    return render_template('view_quiz.html', region=region_key, regions=regions, quiz=quiz, feedback=feedback)

@app.route('/journal/<region>', methods=['GET', 'POST'])
def view_journal(region):
  region_key = region.capitalize()
  regions = data_loader.load_all_regions()

  if request.method == 'POST':
    # collect all textarea inputs (names: q0, q1, q2, …)
    answers = {key: val for key, val in request.form.items()}
    data_loader.update_journal(region_key, answers)
    # Mark this region’s status = true
    data_loader.set_region_status(region_key, True)
    # redirect back to GET so refresh doesn’t repost
    return redirect(url_for('view_journal', region=region.lower()))

  # GET
  questions       = data_loader.get_questions_for_region(region_key) or []
  existing_entries = data_loader.load_journal_answers(region_key)
  # you could prefill with the latest entry if you like:
  latest_answers = existing_entries[-1]['answers'] if existing_entries else {}

  return render_template(
    'view_journal.html',
    region=region_key,
    regions=regions,
    questions=questions,
    latest_answers=latest_answers
  )


if __name__ == '__main__':
    app.run(debug=True, port=5000)
