import json
import os

# Paths to data files
REGIONS_PATH = os.path.join('data', 'regions.json')
JOURNALS_PATH = os.path.join('data', 'journals.json')
QUESTIONS_PATH = os.path.join('data', 'journal_questions.json')
FEEDBACK_PATH = os.path.join('data', 'feedback.json')

# NEW! quiz questions && save answers && enter page time
QUIZ_QUESTIONS_PATH   = os.path.join('data', 'quiz_questions.json')
QUIZ_ANSWERS_PATH   = os.path.join('data', 'quiz_answers.json')

def load_all_regions():
    with open(REGIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_region(region_name):
    all_regions = load_all_regions()
    return all_regions.get(region_name)

def load_all_journals():
    with open(JOURNALS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_journal_questions():
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_questions_for_region(region_name):
    all_questions = load_journal_questions()
    return all_questions.get(region_name)

def load_journal_answers(region_name):
    journals = load_all_journals()
    return journals.get(region_name, [])

def update_journal(region_name, answers):
    journals = load_all_journals()
    new_entry = {
        "answers": answers
    }
    if region_name in journals:
        journals[region_name].append(new_entry)
    else:
        journals[region_name] = [new_entry]
    
    with open(JOURNALS_PATH, 'w', encoding='utf-8') as f:
        json.dump(journals, f, ensure_ascii=False, indent=2)

def clear_journal(region_name):
    journals = load_all_journals()
    if region_name in journals:
        journals[region_name] = []
        
        with open(JOURNALS_PATH, 'w', encoding='utf-8') as f:
            json.dump(journals, f, ensure_ascii=False, indent=2)

def clear_all_journals():
    journals = load_all_journals()
    for region in journals:
        journals[region] = []
    with open(JOURNALS_PATH, 'w', encoding='utf-8') as f:
        json.dump(journals, f, ensure_ascii=False, indent=2)

# ====== New part: feedback functions ======

def load_feedback():
    """Load all multiple-choice feedback."""
    with open(FEEDBACK_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_feedback_for_choice(mp_id, choice_letter):
    """Get feedback text for a given multiple-choice question and choice.

    Args:
        mp_id (str): multiple choice id, e.g., 'mp1'
        choice_letter (str): one of 'A', 'B', 'C', 'D'
    
    Returns:
        str or None: feedback text if found, otherwise None
    """
    feedback_data = load_feedback()
    mp_info = feedback_data.get(mp_id)
    if not mp_info:
        return None
    return mp_info.get(choice_letter)

# ====== New quiz loader functions ======

def load_quiz_questions():
    """Returns entire dict of region → [questions,…]."""
    with open(QUIZ_QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_quiz_for_region(region_name):
    """Return the list of quiz questions for exactly this region."""
    all_q = load_quiz_questions()
    return all_q.get(region_name)

# ── Quiz Answers ──────────────────────────────────────────────────────────
def load_all_quiz_answers():
    with open(QUIZ_ANSWERS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_quiz_answers(region_name):
    return load_all_quiz_answers().get(region_name, [])

def update_quiz_answers(region_name, answers):
    qa = load_all_quiz_answers()
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "answers": answers
    }
    if region_name in qa:
        qa[region_name].append(entry)
    else:
        qa[region_name] = [entry]
    with open(QUIZ_ANSWERS_PATH, 'w', encoding='utf-8') as f:
        json.dump(qa, f, ensure_ascii=False, indent=2)


# ====== New status loader functions ======
def save_all_regions(regions_dict):
    """Overwrite regions.json with the given dict."""
    with open(REGIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(regions_dict, f, ensure_ascii=False, indent=2)

def set_region_status(region_name, status=True):
    """
    Set the `status` field for one region in regions.json.
    """
    regions = load_all_regions()
    if region_name in regions:
        regions[region_name]['status'] = status
        save_all_regions(regions)