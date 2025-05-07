from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os
import re
from utils import data_loader
import secrets

with open(os.path.join("data", "quiz_questions.json"), "r", encoding="utf-8") as f:
    QUIZ_DATA = json.load(f)

with open('data/final_quiz.json', 'r', encoding='utf-8') as f:
    FINAL_QUIZ = json.load(f)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.context_processor
def inject_regions():
    # This makes `regions` available in ALL templates
    return dict(regions=data_loader.load_all_regions())

@app.route('/')
def home():
    return render_template('home.html', hide_top_banner=True, nav_class='nav-home', is_homepage=True)




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
    idx = int(request.args.get('idx', 1))  # default to 1

    with open('data/regions.json', 'r') as f:
        regions = json.load(f)

    quiz = data_loader.get_quiz_for_region(region_key)
    feedback = data_loader.load_feedback()

    return render_template('view_quiz.html',
                           region=region_key,
                           regions=regions,
                           quiz=quiz,
                           feedback=feedback,
                           idx=idx)

@app.route("/learn/<region>/<dish_value>")
def learn_to_cook(region, dish_value):
    # Search all questions in the region for the selected dish
    region_questions = QUIZ_DATA.get(region, [])
    option = next(
        (opt for q in region_questions for opt in q["options"] if opt["value"] == dish_value),
        None
    )

    if not option:
        return "Dish not found", 404

    video_link = option["video_link"]
    raw_label = option["label"]
    dish_label = re.sub(r'^[A-D]\.\s*', '', raw_label)

    return render_template("learn_to_cook.html",
                           region=region,
                           dish_label=dish_label,
                           video_link=video_link)

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

@app.route("/final_quiz/start")
def final_quiz_intro():
    session.pop('final_quiz_score', None)
    session.pop('answered', None)
    return render_template("final_quiz_intro.html", FINAL_QUIZ = FINAL_QUIZ)

@app.route("/final_quiz/question/<int:idx>")
def final_quiz_question(idx):
    with open("data/final_quiz.json", "r", encoding="utf-8") as f:
        FINAL_QUIZ = json.load(f)

    total = len(FINAL_QUIZ)
    if idx < 1 or idx > total:
        return redirect(url_for("final_quiz_intro"))

    question = FINAL_QUIZ[idx - 1]
    selected = request.args.get("selected_region")

    # ✅ Init score and answered state at the beginning
    if idx == 1 and 'final_quiz_score' not in session:
        session['final_quiz_score'] = 0
        session['answered'] = {}

    explanation = None
    is_correct = None

    if selected:
        is_correct = selected == question["correct_region"]
        explanation = question["explanations"].get(selected, "No explanation available.")

        # ✅ Only count score the first time this question is answered
        if str(idx) not in session['answered']:
            session['answered'][str(idx)] = True
            if is_correct:
                session['final_quiz_score'] += 1

    return render_template(
        "final_quiz_question.html",
        question=question,
        idx=idx,
        total=total,
        selected=selected,
        is_correct=is_correct,
        explanation=explanation,
        score=session.get('final_quiz_score', 0)
    )

@app.route("/final_quiz/result")
def final_quiz_result():
    with open("data/final_quiz.json", "r", encoding="utf-8") as f:
        FINAL_QUIZ = json.load(f)

    score = session.get('final_quiz_score', 0)
    total = len(FINAL_QUIZ)

    return render_template("final_quiz_result.html", score=score, total=total)

@app.route("/reset-progress", methods=["POST"])
def reset_progress_route():
    data_loader.reset_progress()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
