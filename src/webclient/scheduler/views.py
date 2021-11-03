from django.shortcuts import render
import json

# Create your views here.
def sf_csv(js):
    parsed = json.loads(js)
    sf_header = "slots,days,minutes_per_slot,start_time,start_date"
    sf_data = f"{parsed['n_timeslots_day']},{parsed['days']},8:00,{parsed['start_date']}"
    return sf_header + "\n" + sf_data

def game_csv(js):
    games = json.loads(js)["games"]
    game_header = "cats,priority,slots/round,rounds"
    game_data = ""
    for g in games:
        game_data += f"{g['name']},{g['n_categories']},{g['priority']},{g['n_timeslots_round']},3\n"
    return game_header + "\n" + game_data

def index(request):
    if request.method == 'POST':
        sf_csv_str = sf_csv(request.body)
        game_csv_str = game_csv(request.body)
        
