from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 초기 데이터 설정
intent_buttons = [
    "search_contents", "search_contents_info", "ranking_chart", "recommend_theme",
    "recommend_similar", "btv_functions", "new_contents", "search_youtube",
    "close_agent", "box_office_contents", "search_channel", "select_contents_number",
    "not_support", "modify_search", "play_music", "search_sports", "set_channel",
    "popular_channel", "sort_recent", "sort_popular", "sort_star_rate", "other_contents",
    "upcoming_release", "free_talk"
]

named_entity_buttons = [
    "title", "program", "genre", "content_type", "channel", "people_name", "people_role",
    "theme", "country", "OTT_name", "season_order", "episode_order", "time_expression",
    "day_of_week", "sort_type", "sports_type", "sports_team", "sports_league",
    "age_rating", "awards", "price", "attendance", "select_number", "running_time",
    "btv_function_name", "keywords", "star_rate"
]

selected_intent = None
selected_named_entities = []
output_json = {}

@app.route('/')
def index():
    return render_template('index.html',
                           intent_buttons=intent_buttons,
                           named_entity_buttons=named_entity_buttons,
                           selected_intent=selected_intent,
                           selected_named_entities=selected_named_entities,
                           output_json=output_json)

@app.route('/select_intent', methods=['POST'])
def select_intent():
    global selected_intent
    selected_intent = request.form['intent']
    update_output_json()
    return jsonify({'result': 'success'})

@app.route('/select_named_entity', methods=['POST'])
def select_named_entity():
    entity = request.form['entity']
    if entity in selected_named_entities:
        selected_named_entities.remove(entity)
    else:
        selected_named_entities.append(entity)
    update_output_json()
    return jsonify({'result': 'success'})

@app.route('/generate_json', methods=['POST'])
def generate_json():
    return jsonify(output_json)

@app.route('/update_output', methods=['POST'])
def update_output():
    global output_json
    new_output = request.form['new_output']
    try:
        output_json = json.loads(new_output)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return jsonify({'result': 'error', 'message': str(e)})
    return jsonify({'result': 'success'})

def update_output_json():
    global output_json
    output_json = {}
    if selected_intent:
        output_json['intent'] = selected_intent
    if selected_named_entities:
        named_entity_dict = {}
        for i, entity in enumerate(selected_named_entities):
            named_entity_dict[entity] = [""]
            output_json['named_entity'] = named_entity_dict

if __name__ == '__main__':
    app.run(debug=True)
