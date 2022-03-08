from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import os
import subprocess

django_path = os.path.dirname(os.path.abspath(__file__))
root = django_path.replace("/scheduler", "") + "/"
data_path = "data/"
model = "model/"

# Create your views here.
def sf_csv(js):
    parsed = json.loads(js)
    sf_header = "slots,days,minutes_per_slot,start_time,start_date,teams"
    sf_data = f"{parsed['n_timeslots_day']},{parsed['days']},{parsed['timeslot_length']},8:00,{parsed['start_date']},{parsed['teams']}"
    return sf_header + "\n" + sf_data

def game_csv(js):
    games = json.loads(js)["games"]
    game_header = "cats,priority,slots/round,rounds"
    game_data = ""
    for g in games:
        game_data += f"{g['name']},{g['n_categories']},{g['priority']},{g['n_timeslots_round']},3\n"
    return game_header + "\n" + game_data

def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()

@csrf_exempt
def index(request):
    if request.method == 'POST':
        sf_csv_str = sf_csv(request.body)
        game_csv_str = game_csv(request.body)
        email = json.loads(request.body)['email']

        file_prefix = email.split('@')[0]

        path_prefix = root + data_path + model
        sf_path = path_prefix + f"{file_prefix}_sf_data.csv"
        game_path = path_prefix + f"{file_prefix}_game_data.csv"

        # debug info
        print(sf_csv_str)
        print(game_csv_str)
        print(sf_path)
        print(game_path)

        # write files to folder
        write_file(sf_path, sf_csv_str)
        write_file(game_path, game_csv_str)

        subprocess.Popen(['python', root + 'main.py', email, sf_path, game_path])
        return HttpResponse(sf_csv_str)
