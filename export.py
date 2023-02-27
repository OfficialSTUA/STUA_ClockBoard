import json, time, datetime, traceback
import dotenv, os, asyncio, requests, csv
import stua_test as stua

ACTIVE_INDEX = 0
ACTIVE_DELAYS_LEN = 0
#DEBUG = True 
#HOLD_DELAYS = False
TIMER = False
RENDER = False
CRIT_RATE = [6, 9, 12, 15, 15]
ANNOUCEMENTS = []
NOTICES = []
ANNOUCEMENTS_INDEX = 0
WIFI = True
TEST = False
SCH = False
SCHMON = ["06:00", "06:30", "07:00", "07:30", "07:40", "07:50", "08:00", "08:10", "08:20", "08:30", "08:40", "09:00", "10:00", "11:00", "12:00"]

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT")) #os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

def get_weekday(num):
    calend = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return calend[num]

def get_schedule():
    response = requests.get("https://pserb-web.vercel.app/api/weekly-schedule")
    with open("sch.json","w") as f:
        f.write(response.text)

get_schedule()

def export_schedule():
    global SCHMON
    global SCH
    output = []
    today = datetime.datetime.now()
    strday = today.strftime("%B p, %Y")
    strtemp = today.strftime("%d")
    if strtemp[0] == "0":
        strtemp = strtemp[1]
    strday = strday.replace("p", strtemp)
    strtime = today.strftime("%H:%M")
    #get_schedule()
    multiplier = 0

    for i in SCHMON:
        if i == strtime and SCH == False:
            get_schedule()
            SCH = True
            multiplier = 0
            break
        else:
            multiplier += 1

    if multiplier > 0:
        SCH = False

    with open("sch.json","r") as f:
        json_obj = json.load(f)
        for day in json_obj["days"]:
            if day["day"] == strday:
                #print(True)
                output.append(f'{day["day"]} - {get_weekday(today.weekday())}')
                output.append(day["block"])
                output.append(day["testing"])
                output.append(day["bell"]["scheduleName"])
                
                period = None

                for time in day["bell"]["schedule"]:
                    if (today <= datetime.datetime.strptime(f'{day["day"]} {time["startTime"]}', "%B %d, %Y %H:%M")):
                        right = str(int((datetime.datetime.strptime(f'{day["day"]} {time["startTime"]}', "%B %d, %Y %H:%M") - today).total_seconds()/60))
                        left = str(int(day["bell"]["schedule"][day["bell"]["schedule"].index(time)-1]["duration"]) - int(right))
                        #print(left)
                        #print(right)
                        #print((datetime.datetime.strptime(f'{day["day"]} {time["startTime"]}', "%B %d, %Y %H:%M") - today).total_seconds()/60)
                        #print((datetime.datetime.strptime(f'{day["day"]} {time["startTime"]}', "%B %d, %Y %H:%M") - today))
                        #print(today)
                        #print(datetime.datetime.strptime(f'{day["day"]} {time["startTime"]}', "%B %d, %Y %H:%M"))
                        #print(datetime.datetime.now())
                        #day["bell"]["schedule"].index(time)
                        period = (day["bell"]["schedule"][day["bell"]["schedule"].index(time)-1]["name"])
                        periodt = (day["bell"]["schedule"][day["bell"]["schedule"].index(time)]["startTime"])
                        #print(periodt)
                        #print(period)
                        break
                #print(output)
                if period == None:
                    period = "After School"
                    left = "--"
                    right = "--"
                    periodt = "--"
                
                output.append(period)
                output.append(day["day"])
                output.append(day["bell"]["schedule"][-8]["startTime"])
                output.append(left)
                output.append(right)
                output.append(periodt)
                #print(left)
                #output.append("21:15")
                #print(day["bell"]["schedule"][-8])
    if output == []:
        output.append(f'{strday} - {get_weekday(today.weekday())}')
        output.append("N/A")
        output.append("No Testing")
        output.append("No School/Special Schedule")
        output.append("Period --")
        output.append(strday)
        output.append("12:00")
        output.append("--")
        output.append("--")
        output.append("No School")
    return output
        

print(export_schedule())

def get_annoucements():
    global ANNOUCEMENTS
    global NOTICES
    ANNOUCEMENTS = []
    NOTICES = []
    with open("static/announcements.txt","r") as f:
        f_read = f.read().split("\n")
        for item in f_read:
            target = item[0]
            if target == "#":
                continue
            item_fin = []
            #print(item)
            item_front = item[0:item.index(":")].split(" ")
            item_front = [i.replace("_"," ") for i in item_front]
            #print(item_front)
            item_back = item[item.index(":")+1:]
            item_fin.append(item_front)
            item_fin.append(item_back)
            #export.append(item_fin)
            if target == "/":
                ANNOUCEMENTS.append(item_fin)
            else:
                NOTICES.append(item_fin)
        #ANNOUCEMENTS = export
            #print(item)
        #print(str(ANNOUCEMENTS) + " GET")
    #print(f_read)

def get_timer():
    global TIMER
    return TIMER

def wifi_disconnect():
    try:
        #print("WAIT")
        response = requests.get("https://new.mta.info/", timeout=50)
        #print("CLEAR")
        return False
    except Exception as e:
        #print(e.message)
        with open("errors.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}: {str(traceback.format_exc())}\n----------")
        return True

def refresh():
    global CRIT_RATE
    global WIFI
    global RENDER
    global PROGRESS
    global TEST
    global ANNOUCEMENTS
    sch = export_schedule()
    load_status = ""
    if wifi_disconnect() == True:
        load_status = "OFFLINE"
        WIFI = False
    elif wifi_disconnect() == False and WIFI == False:
        WIFI = True
        RENDER = False
        #PROGRESS = 0.0
        stua.reset_loading_bar()
    elif render() == False:
        load_status = "RENDER"
    else:
        if (datetime.datetime.today() < datetime.datetime.strptime(f"{sch[5]} {sch[6]}", "%B %d, %Y %H:%M")) and (TEST == False):
            load_status = "SCH"
        else:
            load_status = "DISPLAY"

    copyANON = [i.copy() for i in ANNOUCEMENTS]
    #print(str(ANNOUCEMENTS) + " REF")
    #copyANON = [""]
    if copyANON == [""]:
        copyANON = []

    for item in copyANON:
        while item[1].find("[") != -1:
            index1 = item[1].index("[")
            index2 = item[1].index("]")
            item[1] = item[1].replace(item[1][index1:index2+1], f'<img src="/static/svg/{item[1][index1+1:index2].lower()}.svg" style="height: 5.5vh; margin-bottom: 1%;">')

    json_string = {
        "load_status": str(load_status),
        "load_progress": str(stua.get_loading_bar()),
        "seventh": str(CRIT_RATE[0]),
        "eighth": str(CRIT_RATE[1]),
        "broadway": str(CRIT_RATE[2]),
        "nassau": str(CRIT_RATE[3]),
        "lexington": str(CRIT_RATE[4]),
        "lirr": "25",
        "sch_day": sch[0],
        "sch_block": sch[1],
        "sch_testing": sch[2],
        "sch_sch": sch[3],
        "sch_period": f'This Period is: <strong>{sch[4]}</strong>',
        "sch_left": f'<strong>{sch[7]}</strong>',
        "sch_right": f'<strong>{sch[8]}</strong>',
        "sch_end": f'Ending At: <strong>{sch[9]}</strong>',
        "sch_anon": copyANON
    }
    
    return json.dumps(json_string)

def render(change=False):
    global RENDER
    if RENDER == True:
        return True
    if change == True:
        RENDER = True
        return True
    return False

def timer():
    time.sleep(4)
    global TIMER
    if TIMER == True:
        TIMER = False
    else:
        TIMER = True
    return TIMER

def delay_update(current=False):
    global TIMER
    global ACTIVE_DELAYS_LEN
    if current == True:
        return ACTIVE_DELAYS_LEN
    if TIMER == True:
        return ACTIVE_DELAYS_LEN
    else:
        return -1

"""
def delay_lock(current=False):
    global HOLD_DELAYS
    global RENDER
    if RENDER == False:
        return False
    if current == True:
        HOLD_DELAYS = False
    return HOLD_DELAYS
"""

def sort_char(input):
    ord_input = [ord(i) for i in input if len(i) == 1]
    ord_input = sorted(ord_input)
    output = [chr(i) for i in ord_input]
    #print(input)
    for i in input:
        if i not in output:
            output.append(i)
    return output

def branch(terminus):
    if terminus == "Ozone Park-Lefferts Blvd":
        return "OP"
    elif terminus == "Far Rockaway-Mott Av":
        return "FR"
    elif terminus == "Rockaway Park-Beach 116 St":
        return "OP"

def delay():
    #print("delay req received")
    global DELAYS
    global ACTIVE_INDEX
    global ACTIVE_DELAYS_LEN
    global TIMER
    global RENDER
    global HOLD_DELAYS
    global ANNOUCEMENTS
    global ANNOUCEMENTS_INDEX
    global NOTICES
    delays_export = []
    emblems = []
    emblems_str = ""
    delays = stua.alertsSubway(planned=False)
    #delays = []
    for item in NOTICES:
        delays.append(item)

    for item in delays:
        for pic in item[0]:
            if pic not in emblems:
                emblems.append(pic)
    emblems = sort_char(emblems)
    for item in emblems:
        emblems_str += f'<div style="float: left; height: 5.5vh; width: fit-content; margin: 4px;"><img src="/static/svg/{item.lower()}.svg" style="height: inherit;"></div>'
    #delays=[]
    get_annoucements()
    if ANNOUCEMENTS == []:
        ANNOUCEMENTS = ['']
    #ANNOUCEMENTS = ['']
    #delays.append([['D','B'], '[B][D] trains are running with delays in both directions after we restored a loss of third rail power near 145 St.'])
    if (len(delays) == 0) and (ANNOUCEMENTS == ['']):
        ACTIVE_DELAYS_LEN = 0
        delays_export.append(len(delays))
        for i in range(7):
            delays_export.append("")
            print("delays done")
        return delays_export
    else:
        #get_annoucements()
        if ANNOUCEMENTS == ['']:
            grouped_delays = [delays[n:n+2] for n in range(0, len(delays), 2)]
        else:
            grouped_delays = [delays[n:n+1] for n in range(0, len(delays), 1)]
        #print(len(grouped_delays))
        #print(grouped_delays)
        #print(f"ACTIVE INDEX: {ACTIVE_INDEX}")
        #print(f"LEN DELAYS: {len(grouped_delays)}")
        #ACTIVE_DELAYS_LEN = len(grouped_delays)
        if ACTIVE_INDEX + 1 >= len(grouped_delays):
            ACTIVE_INDEX = 0
        else:
            ACTIVE_INDEX = ACTIVE_INDEX + 1
        #print(grouped_delays)
        DELAYS = []
        if len(grouped_delays) == 0:
            DELAYS = []
        else:
            DELAYS = grouped_delays[ACTIVE_INDEX]

        #print(ANNOUCEMENTS)
        #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
        if ANNOUCEMENTS == ['']:
            pass
        else:

            if ANNOUCEMENTS_INDEX + 1 >= len(ANNOUCEMENTS):
                ANNOUCEMENTS_INDEX = 0
            else:
                ANNOUCEMENTS_INDEX = ANNOUCEMENTS_INDEX + 1
            #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
            annoucement = [i.copy() for i in ANNOUCEMENTS]
            #print(id(annoucement[ANNOUCEMENTS_INDEX]))
            #print(id(ANNOUCEMENTS[ANNOUCEMENTS_INDEX]))
            #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
            DELAYS.insert(0, annoucement[ANNOUCEMENTS_INDEX])
        #print(DELAYS)
        #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
        #print(DELAYS)
        #print(DELAYS)
        #DELAYS = DELAYS[0]
        #print(str(ANNOUCEMENTS) + " DEL")
        #if TIMER == False:
            #HOLD_DELAYS = True
        ACTIVE_DELAYS_LEN = len(DELAYS)
        #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
        if len(DELAYS) == 1:
            #print(4)
            delays_export.append(len(DELAYS))
            large_emblem_str = ""
            #print(DELAYS[0])
            #DELAYS[0][0].append(DELAYS[0][0][0])
            DELAYS[0][0] = sort_char(DELAYS[0][0])
            #print(DELAYS[0])
            for item in DELAYS[0][0]:
                #print(item)
                #print(4)
                large_emblem_str += f'<div style="margin-bottom: 2%; margin-left: 1%; margin-right: 1%;"><img src="/static/svg/{item.lower()}.svg" style="height: 25vh; width: 100%; flex: auto;"></div>'
            for DELAY in DELAYS:
                #print(DELAY)
                while DELAY[1].find("[") != -1:
                    index1 = DELAY[1].index("[")
                    index2 = DELAY[1].index("]")
                    DELAY[1] = DELAY[1].replace("\n\n", "<br>")
                    DELAY[1] = DELAY[1].replace("\n", "<br>")
                    #print(DELAY[1])
                    DELAY[1] = DELAY[1].replace(DELAY[1][index1:index2+1], f'<img src="/static/svg/{DELAY[1][index1+1:index2].lower()}.svg" style="height: 17.5%; margin-bottom: 1%;">')
            delays_export.append(large_emblem_str)
            delays_export.append(DELAYS[0][1])
            #print(delays_export)
            for i in range(3):
                delays_export.append("")
            #print(delays_export)
            print("delays done")
            """
            while TIMER == True:
                if RENDER == True:
                    time.sleep(0.5)
                else:
                    break
            """
            #print(str(ANNOUCEMENTS) + " DEL FIN1")
            delays_export.append(emblems_str)
            delays_export.append(f"{ACTIVE_INDEX+1}/{len(grouped_delays)}")
            return delays_export
        else:
            #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
            delays_export.append(len(DELAYS))
            #DELAYS[0][1] = DELAYS[0][1] + "EEEE"
            #print(ANNOUCEMENTS)
            for DELAY in DELAYS:
                while DELAY[1].find("[") != -1:
                    index1 = DELAY[1].index("[")
                    index2 = DELAY[1].index("]")
                    DELAY[1] = DELAY[1].replace(DELAY[1][index1:index2+1], f'<img src="/static/svg/{DELAY[1][index1+1:index2].lower()}.svg" style="height: 5.5vh; margin-bottom: 1%;">')
            #print(ANNOUCEMENTS)
            for i in range(2):
                delays_export.append("")
            for item in DELAYS:
                delays_export.append(item[1])
            #print(delays_export)
            if len(delays_export) != 6:
                delays_export.append("")

            """
            while TIMER == True:
                if RENDER == True:
                    time.sleep(0.5)
                else:
                    break
            """
            #print(str(ANNOUCEMENTS) + " DEL FIN2")
            print("delays done")
            delays_export.append(emblems_str)
            delays_export.append(f"{ACTIVE_INDEX+1}/{len(grouped_delays)}")
            return delays_export

#delay()

def subway():

    global CRIT_RATE

    seventh_ave_crit = CRIT_RATE[0]
    eighth_avenue_crit = CRIT_RATE[1]
    broadway_crit = CRIT_RATE[2]
    nassau_crit = CRIT_RATE[3]
    lexington_avenue_crit = CRIT_RATE[4]

    masterlistSUBWAY = stua.gtfsSubwayBATCHED([("137", "N", 1, seventh_ave_crit, "NONE"), ("137", "N", 2, seventh_ave_crit, "NONE"), ("137", "N", 3, seventh_ave_crit, "NONE"), ("137", "N", 4, seventh_ave_crit, "NONE"), ("137", "N", 5, seventh_ave_crit, "NONE"), #0-4
                                        ("137", "S", 1, seventh_ave_crit, "NONE"), ("137", "S", 2, seventh_ave_crit, "NONE"), ("137", "S", 3, seventh_ave_crit, "NONE"), ("137", "S", 4, seventh_ave_crit, "NONE"), ("137", "S", 5, seventh_ave_crit, "NONE"), #5-9
                                        ("A34", "N", 1, eighth_avenue_crit, "NONE"), ("A34", "N", 2, eighth_avenue_crit, "NONE"), ("A34", "N", 3, eighth_avenue_crit, "NONE"), ("A34", "N", 4, eighth_avenue_crit, "NONE"), ("A34", "N", 5, eighth_avenue_crit, "NONE"), #10-14
                                        ("A36", "S", 1, eighth_avenue_crit, "NONE"), ("A36", "S", 2, eighth_avenue_crit, "NONE"), ("A36", "S", 3, eighth_avenue_crit, "NONE"), ("A36", "S", 4, eighth_avenue_crit, "NONE"), ("A36", "S", 5, eighth_avenue_crit, "NONE"), #15-19
                                        ("R24", "N", 1, broadway_crit, "NONE"), ("R24", "N", 2, broadway_crit, "NONE"), #20-21
                                        ("R28", "S", 1, broadway_crit, "NONE"), ("R28", "S", 2, broadway_crit, "NONE"), #22-23
                                        ("M21", "N", 1, nassau_crit, "NONE"), ("M21", "N", 2, nassau_crit, "NONE"), #24-25
                                        ("640", "N", 1, lexington_avenue_crit, "NONE"), ("640", "N", 2, lexington_avenue_crit, "NONE"), ("640", "N", 3, lexington_avenue_crit, "NONE"), ("640", "N", 4, lexington_avenue_crit, "NONE")]) #26-29
    return masterlistSUBWAY

def bus():
    masterlistBUS = stua.gtfsBusBATCHED([("404969", 0, 1, 1, "NONE"), ("404969", 0, 2, 1, "NONE"), #0-1
                                        ("803147", 0, 1, 2, "NONE"), ("803147", 0, 2, 2, "NONE"), #2-3
                                        ("404238", 1, 1, 7, "SIM1"), ("404238", 1, 2, 7, "SIM1"), ("404238", 1, 1, 7, "SIM2"), ("404238", 1, 2, 7, "SIM2"), #4-7
                                        ("404225", 1, 1, 7, "X27"), ("404225", 1, 2, 7, "X27"), ("404225", 1, 1, 7, "X28"), ("404225", 1, 2, 7, "X28"), ("405065", 0, 1, 1, "M20"), ("405065", 0, 2, 1, "M20"), ("903013", 1, 1, 6, "SIM7"), ("903013", 1, 2, 6, "SIM7"), #8-15
                                        ("903013", 1, 1, 6, "SIM33"), ("903013", 1, 2, 6, "SIM33"), ("404219", 1, 1, 7, "SIM34"), ("404219", 1, 2, 7, "SIM34")]) #16-19
    return masterlistBUS

def lirr():
    print("lirr done")
    masterlistLIRR = []
    for i in range(3):
        masterlistLIRR.append(stua.gtfsLIRR())

    masterlistLIRR[0].get(("237", "0", 1, 25, ["Port Washington", "Hempstead"]))
    masterlistLIRR[1].get(("241", "0", 1, 25, []))
    masterlistLIRR[2].get(("349", "0", 1, 25, ["Port Washington", "Hempstead"]))

    return masterlistLIRR

#print(lirr())

def modlirrTIME(input):
    if type(input) == str:
        return "00:00"
    t = input.strftime("%I:%M %p")
    if t[0] == "0":
        t = t[1:]
    #print(t)
    return t

def export_lirr():
    masterlistLIRR = lirr()
    #print("lirr done")
    json_string = {
        "lirr": {
            "crit": [f"{masterlistLIRR[0].time}", f"{masterlistLIRR[1].time}", f"{masterlistLIRR[2].time}"],
            "time": [f"{modlirrTIME(masterlistLIRR[0].core_time)}", f"{modlirrTIME(masterlistLIRR[1].core_time)}", f"{modlirrTIME(masterlistLIRR[2].core_time)}"],
            "branch": [f'<img src="/static/svg/{masterlistLIRR[0].route_id}.svg" style="height: 85%; margin-top: 5%;"><h1 id="penn" class="branch">PENN</h1>', f'<img src="/static/svg/{masterlistLIRR[1].route_id}.svg" style="height: 85%; margin-top: 5%;"><h1 id="penn" class="branch">ATLN</h1>', f'<img src="/static/svg/{masterlistLIRR[2].route_id}.svg" style="height: 85%; margin-top: 5%;"><h1 id="penn" class="branch">GCM</h1>'],
            "dest": [f'To {masterlistLIRR[0].terminus}, making stops at:', f'To {masterlistLIRR[1].terminus}, making stops at:', f'To {masterlistLIRR[2].terminus}, making stops at:'],
            "stops": [f"{' - '.join(masterlistLIRR[0].station_name_list)}", f"{' - '.join(masterlistLIRR[1].station_name_list)}", f"{' - '.join(masterlistLIRR[2].station_name_list)}"]
        }
    }
    return json.dumps(json_string)

#print(export_lirr())

def export():
    
    #print(delay_get)
    #print(DELAYS)
    #print("req received")
    masterlistSUBWAY = subway()
    print("subway done")
    masterlistBUS = bus()
    print("bus done")
    #masterlistLIRR = lirr()
    #print("lirr done")
    #print("req parsed")
    #delay_get = delay()
    #print("delays done")
    json_string = {
        "left_side": {
            "uptown_seventh": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[0].route_id).lower()}.svg' style='height: 92%;'>",
                "time": f"{masterlistSUBWAY[0].time} minutes",
                "terminus": f"{masterlistSUBWAY[0].terminus}"
            },
            "downtown_seventh": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[5].route_id).lower()}.svg' style='height: 92%;'>",
                "time": f"{masterlistSUBWAY[5].time} minutes",
                "terminus": f"{masterlistSUBWAY[5].terminus}"
            },
            "uptown_eighth": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[10].route_id).lower()}.svg' style='height: 92%;'>",
                "time": f"{masterlistSUBWAY[10].time} minutes",
                "terminus": masterlistSUBWAY[10].terminus
            },
            "downtown_eighth": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[15].route_id).lower()}.svg' style='height: 92%;'>",
                "time": f"{masterlistSUBWAY[15].time} minutes",
                "terminus": masterlistSUBWAY[15].terminus
            },
            "uptown_broadway": {
                "large": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[20].route_id).lower()}.svg' style='height: 92%;'>",
                    "time": f"{masterlistSUBWAY[20].time} minutes",
                    "terminus": masterlistSUBWAY[20].terminus
                },
                "small": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[21].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
                    "time": f"{masterlistSUBWAY[21].time}m",
                    "terminus": branch(masterlistSUBWAY[21].terminus)
                }
            
            }
        },
        "right_side_standard": {
            "uptown_seventh": {
                "one": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[1].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[1].time}m",
                    "branch": branch(masterlistSUBWAY[1].terminus)
                },
                "two": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[2].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[2].time}m",
                    "branch": branch(masterlistSUBWAY[2].terminus)
                },
                "three": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[3].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[3].time}m",
                    "branch": branch(masterlistSUBWAY[3].terminus)
                },
                "four": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[4].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[4].time}m",
                    "branch": branch(masterlistSUBWAY[4].terminus)
                }
            },
            "downtown_seventh": {
                "one": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[6].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[6].time}m",
                    "branch": branch(masterlistSUBWAY[6].terminus)
                },
                "two": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[7].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[7].time}m",
                    "branch": branch(masterlistSUBWAY[7].terminus)
                },
                "three": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[8].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[8].time}m",
                    "branch": branch(masterlistSUBWAY[8].terminus)
                },
                "four": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[9].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[9].time}m",
                    "branch": branch(masterlistSUBWAY[9].terminus)
                }
            },
            "uptown_eighth": {
                "one": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[11].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[11].time}m",
                    "branch": branch(masterlistSUBWAY[11].terminus)
                },
                "two": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[12].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[12].time}m",
                    "branch": branch(masterlistSUBWAY[12].terminus)
                },
                "three": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[13].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[13].time}m",
                    "branch": branch(masterlistSUBWAY[13].terminus)
                },
                "four": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[14].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[14].time}m",
                    "branch": branch(masterlistSUBWAY[14].terminus)
                }
            },
            "downtown_eighth": {
                "one": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[16].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[16].time}m",
                    "branch": branch(masterlistSUBWAY[16].terminus)
                },
                "two": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[17].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[17].time}m",
                    "branch": branch(masterlistSUBWAY[17].terminus)
                },
                "three": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[18].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[18].time}m",
                    "branch": branch(masterlistSUBWAY[18].terminus)
                },
                "four": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[19].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[19].time}m",
                    "branch": branch(masterlistSUBWAY[19].terminus)
                }
            },
            "downtown_broadway": {
                "large": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[22].route_id).lower()}.svg' style='height: 92%;'>",
                    "time": f"{masterlistSUBWAY[22].time} minutes",
                    "terminus": masterlistSUBWAY[22].terminus
                },
                "small": {
                    "emblem": f'<img src="/static/svg/{(masterlistSUBWAY[23].route_id).lower()}.svg" style="height: 90%; margin-left: 7px; margin-top: 5%;">',
                    "time": f"{masterlistSUBWAY[23].time}m",
                    "branch": branch(masterlistSUBWAY[23].terminus)
                }
            }
        },
        "bottom_side": {
            "uptown_nassau": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[24].route_id).lower()}.svg' style='height: 75%; margin-left: 7px; margin-top: 6%;'>",
                    "time": f"{masterlistSUBWAY[24].time}m",
                    "branch": branch(masterlistSUBWAY[24].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[25].route_id).lower()}.svg' style='height: 75%; margin-left: 7px; margin-top: 5.5%;'>",
                    "time": f"{masterlistSUBWAY[25].time}m",
                    "branch": branch(masterlistSUBWAY[25].terminus)
                }
            },
            "uptown_lex": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[26].route_id).lower()}.svg' style='height: 75%; margin-left: 7px; margin-top: 6%;'>",
                    "time": f"{masterlistSUBWAY[26].time}m",
                    "branch": branch(masterlistSUBWAY[26].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[27].route_id).lower()}.svg' style='height: 75%; margin-left: 7px; margin-top: 5.5%;'>",
                    "time": f"{masterlistSUBWAY[27].time}m",
                    "branch": branch(masterlistSUBWAY[27].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[28].route_id).lower()}.svg' style='height: 75%; margin-left: 7px; margin-top: 5.5%;'>",
                    "time": f"{masterlistSUBWAY[28].time}m",
                    "branch": branch(masterlistSUBWAY[28].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[29].route_id).lower()}.svg' style='height: 75%; margin-left: 7px; margin-top: 5.5%;'>",
                    "time": f"{masterlistSUBWAY[29].time}m",
                    "branch": branch(masterlistSUBWAY[29].terminus)
                }
            },
            "bus": {
                "one": {
                    "route": masterlistBUS[0].route_id,
                    "time": f"{masterlistBUS[0].time}, {masterlistBUS[1].time}m"
                },
                "two": {
                    "route": masterlistBUS[2].route_id,
                    "time": f"{masterlistBUS[2].time}, {masterlistBUS[3].time}m"
                },
                "three": {
                    "route": "SIM1",
                    "time": f"{masterlistBUS[4].time}, {masterlistBUS[5].time}m"
                },
                "four": {
                    "route": "SIM2",
                    "time": f"{masterlistBUS[6].time}, {masterlistBUS[7].time}m"
                },
                "five": {
                    "route": "X27",
                    "time": f"{masterlistBUS[8].time}, {masterlistBUS[9].time}m"
                },
                "six": {
                    "route": "X28",
                    "time": f"{masterlistBUS[10].time}, {masterlistBUS[11].time}m"
                },
                "seven": {
                    "route": "M20",
                    "time": f"{masterlistBUS[12].time}, {masterlistBUS[13].time}m"
                },
                "eight": {
                    "route": "SIM7",
                    "time": f"{masterlistBUS[14].time}, {masterlistBUS[15].time}m"
                },
                "nine": {
                    "route": "SIM33",
                    "time": f"{masterlistBUS[16].time}, {masterlistBUS[17].time}m"
                },
                "ten": {
                    "route": "SIM34",
                    "time": f"{masterlistBUS[18].time}, {masterlistBUS[19].time}m"
                }
            }
        }
    }

    print("exported")

    return json.dumps(json_string)   

#get_annoucements()
#print(NOTICES)

