import os
import json
import requests
import json
import datetime

from django.http import JsonResponse
from django.utils import timezone

cache_time = "Never"
vakt_cache_tuples = ""
vakt_cache_json = ""
def hent_vaktliste(output="json"):
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    vaktliste = os.path.join(cur_dir, "vaktliste.json")
    with open(vaktliste,"r") as f:
        return json.loads(f.read())
    """
    global vakt_cache_tuples
    global vakt_cache_json
    global cache_time
    if vakt_cache_json=="" or timezone.now()-cache_time>=datetime.timedelta(hours=12):
        print("Cacher vaktliste")
        vakt_data = requests.get("https://script.googleusercontent.com/macros/echo?user_content_key=gR05slZZQrkrumxUc8DJZEc81FUEXWJpVDu8OGmYc7Bd8STD9BEvHnNLn3Hqa93sZAkXhzOJJfVsxRBCis22hxj50ZyEv7V0m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnBHVJ4Ip7UlCqkboOF3idyLswydE_Rh_IZ2xA43kME624RrB2b1T6_LZIUQtyudpTtsAUXIaJqQ5&lib=MvQgEbo5GAfi_xTmCXLhSAK0T_1fexhuo").json()
        
        vakt_data_tuples = []
        for day in vakt_data:
            for time in vakt_data[day]:
                vakt_data_tuples.append((day,time,vakt_data[day][time]))

        cache_time = timezone.now()
        vakt_cache_tuples = vakt_data_tuples
        vakt_cache_json = vakt_data
        if output=="tuples":
            return vakt_data_tuples
        else:
            return vakt_data_json
    else:
        print("Bruker cachet vaktliste")
        if output=="tuples":
            return vakt_cache_tuples
        else:
            return vakt_cache_json

def person_match(l,f):
    s = "".join(l).lower()
    for pf in f:
        if pf in s:
            return True
    return False

def vakt_filter(days="",times="",persons="",full=True,compact=False):
    filter_data = {}
    filter_times = []
    filter_days = [d.title() for d in days.split(",") if d!='']
    filter_persons = [p.lower() for p in persons.split(",") if p!='']
    for time in times.split(","):
        #HERE BE DRAGONS
        if time!='':
            time_slots = ["10:15 - 12:07","12:07 - 14:07", "14:07 - 16:07", "16:07 - 18:00"]
            if ":" in time:
                h,m = map(int,time.split(":"))
            elif "." in time:
                h,m = map(int,time.split("."))
            else:
                h=int(time)
                m=0
            timeslot = ""
            #WHY ARE YOU STILL HERE
            if h>=18:
                filter_times.append("16:07 - 18:00")
            elif h<10:
                filter_times.append("10:15 - 12:07")
            else:
                for t in range(10,18,2):
                    if h in range(t,t+2):
                        #AAAAAAAAAAAAAAAAAAAAH
                        if h==t and m<7:
                            filter_times.append(time_slots[max(0,(t-10)//2-1)])
                        else:
                            filter_times.append(time_slots[(t-10)//2])
        #THE DRAGONS ARE GONE
    vakt_data = hent_vaktliste(output="tuples") 
    for vakt in [v for v in vakt_data if (not filter_days or v[0] in filter_days or v[0][:3] in filter_days) and (not filter_times or v[1] in filter_times) and (not filter_persons or person_match(v[2],filter_persons))]:
        day,time_slot,hackers = vakt
        if compact:
            day = days[:3]
            time_slot = "".join(time_slot.split(" "))
        if day not in filter_data:
            filter_data[day] = {}
        if full:
            filter_data[day][time_slot] = hackers
        else:
           for hacker in [pm for pm in hackers for pf in filter_persons if pf in pm.lower()]:
                if time_slot not in filter_data[day]:
                    filter_data[day][time_slot] = []
                filter_data[day][time_slot].append(hacker)

    return filter_data

def vakter(request):
    dager = request.GET.get('dag','')
    tider = request.GET.get('tid','')
    personer = request.GET.get('person','')
    full = request.GET.get('full','')
    compact = request.GET.get('compact','')
    if full=="False": 
        full = False
    else:
        full = True
    if compact=="True": 
        compact = True
    else:
        compact = False
    vakt_data = vakt_filter(days=dager,times=tider,persons=personer,full=full,compact=compact)
    return JsonResponse(vakt_data)

def current(request):
    days = ["Søndag","Mandag","Tirsdag","Onsdag","Torsdag","Fredag","Lørdag"]
    day,time = datetime.datetime.strftime(datetime.datetime.now(),"%w,%H:%M").split(",")
    return JsonResponse(vakt_filter(days=days[int(day)],times=time))
