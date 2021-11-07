from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import os
import subprocess

django_path = os.path.dirname(os.path.abspath(__file__))
root = django_path.replace("webclient/scheduler", "")
data_path = "data/"
model = "model/"

# Create your views here.
def sf_csv(js):
    parsed = json.loads(js)
    sf_header = "slots,days,minutes_per_slot,start_time,start_date"
    sf_data = f"{parsed['n_timeslots_day']},{parsed['days']},{parsed['timeslot_length']},8:00,{parsed['start_date']}"
    return sf_header + "\n" + sf_data

def game_csv(js):
    games = json.loads(js)["games"]
    game_header = "cats,priority,slots/round,rounds"
    game_data = ""
    for g in games:
        game_data += f"{g['name']},{g['n_categories']},{g['priority']},{g['n_timeslots_round']},3\n"
    return game_header + "\n" + game_data

@csrf_exempt
def index(request):
    if request.method == 'POST':
        sf_csv_str = sf_csv(request.body)
        game_csv_str = game_csv(request.body)
        print(sf_csv_str)
        print(game_csv_str)
        print(root + data_path + model + "big_game_data.csv")
        print(root + data_path + model + "big_sf_data.csv")
        sf_csv_file = open(root + data_path + model + "big_sf_data.csv", "w")
        sf_csv_file.write(sf_csv_str)
        sf_csv_file.close()
        game_csv_file = open(root + data_path + model + "big_game_data.csv", "w")
        game_csv_file.write(game_csv_str)
        game_csv_file.close()
        email = json.loads(request.body)['email']
        subprocess.Popen(['python', root + '/main.py', email])
        return HttpResponse(sf_csv_str)
