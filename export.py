import stua, json, time
import dotenv, os, asyncio

ACTIVE_INDEX = 0
ACTIVE_DELAYS_LEN = 0
TIMER = True
RENDER = False

dotenv.load_dotenv()
stua.keyMTA(os.getenv("NYCT")) #os.getenv("NYCT"))
stua.keyBUSTIME(os.getenv("BusTime"))

def render(change=False):
    global RENDER
    if RENDER == True:
        return True
    if change == True:
        RENDER = True
        return True
    return False

def timer():
    time.sleep(6)
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

def branch(terminus):
    if terminus == "Ozone Park-Lefferts Blvd":
        return "OP"
    elif terminus == "Far Rockaway-Mott Av":
        return "FR"
    elif terminus == "Rockaway Park-Beach 116 St":
        return "OP"

def delay():
    global DELAYS
    global ACTIVE_INDEX
    global ACTIVE_DELAYS_LEN
    global TIMER
    global RENDER
    delays_export = []
    delays = stua.alertsSubway(planned=False)
    #delays = delays[:2]
    if len(delays) == 0:
        ACTIVE_DELAYS_LEN = 0
        delays_export.append(len(delays))
        for i in range(5):
            delays_export.append("")
        return delays_export
    else:
        grouped_delays = [delays[n:n+3] for n in range(0, len(delays), 3)]
        #print(f"ACTIVE INDEX: {ACTIVE_INDEX}")
        #print(f"LEN DELAYS: {len(grouped_delays)}")
        #ACTIVE_DELAYS_LEN = len(grouped_delays)
        if ACTIVE_INDEX + 1 >= len(grouped_delays):
            ACTIVE_INDEX = 0
        else:
            ACTIVE_INDEX = ACTIVE_INDEX + 1
        DELAYS = grouped_delays[ACTIVE_INDEX]
        ACTIVE_DELAYS_LEN = len(DELAYS)
        #print(len(DELAYS))
        if len(DELAYS) == 1:
            #print(4)
            delays_export.append(len(DELAYS))
            large_emblem_str = ""
            for item in DELAYS[0][0]:
                #print(4)
                large_emblem_str += f'<div style="margin-bottom: 2%; margin-left: 1%; margin-right: 1%;"><img src="/static/svg/{item.lower()}.svg" style="height: 30vh; width: 100%; flex: auto;"></div>'
            for DELAY in DELAYS:
                while DELAY[1].find("[") != -1:
                    index1 = DELAY[1].index("[")
                    index2 = DELAY[1].index("]")
                    DELAY[1] = DELAY[1].replace(DELAY[1][index1:index2+1], f'<img src="/static/svg/{DELAY[1][index1+1:index2].lower()}.svg" style="height: 15%; margin-bottom: 1%;">')
            delays_export.append(large_emblem_str)
            delays_export.append(DELAYS[0][1])
            #print(delays_export)
            for i in range(3):
                delays_export.append("")
            #print(delays_export)
            """
            while TIMER == True:
                if RENDER == True:
                    time.sleep(0.5)
                else:
                    break
            """
            return delays_export
        else:
            delays_export.append(len(DELAYS))
            for DELAY in DELAYS:
                while DELAY[1].find("[") != -1:
                    index1 = DELAY[1].index("[")
                    index2 = DELAY[1].index("]")
                    DELAY[1] = DELAY[1].replace(DELAY[1][index1:index2+1], f'<img src="/static/svg/{DELAY[1][index1+1:index2].lower()}.svg" style="height: 6vh; margin-bottom: 1%;">')
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
            return delays_export

def subway():

    seventh_ave_crit = 4
    eighth_avenue_crit = 9
    broadway_crit = 12
    nassau_crit = 12
    lexington_avenue_crit = 12

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

def export():
    
    delay_get = delay()
    #print(delay_get)
    #print(DELAYS)
    #print("req received")
    masterlistSUBWAY = subway()
    masterlistBUS = bus()
    #print("req parsed")
    json_string = {
        "delay_count": delay_get[0],
        "left_side": {
            "uptown_seventh": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[0].route_id).lower()}.svg' style='height: 97%;'>",
                "time": f"{masterlistSUBWAY[0].time} minutes",
                "terminus": f"{masterlistSUBWAY[0].terminus}"
            },
            "downtown_seventh": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[5].route_id).lower()}.svg' style='height: 97%;'>",
                "time": f"{masterlistSUBWAY[5].time} minutes",
                "terminus": f"{masterlistSUBWAY[5].terminus}"
            },
            "uptown_eighth": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[10].route_id).lower()}.svg' style='height: 97%;'>",
                "time": f"{masterlistSUBWAY[10].time} minutes",
                "terminus": masterlistSUBWAY[10].terminus
            },
            "downtown_eighth": {
                "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[15].route_id).lower()}.svg' style='height: 97%;'>",
                "time": f"{masterlistSUBWAY[15].time} minutes",
                "terminus": masterlistSUBWAY[15].terminus
            },
            "uptown_broadway": {
                "large": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[20].route_id).lower()}.svg' style='height: 97%;'>",
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
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[22].route_id).lower()}.svg' style='height: 97%;'>",
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
        "right_side_onedelay": {
            "emblem": delay_get[1],
            "delay": delay_get[2]
        },
        "right_side_multipledelay": {
            "one": delay_get[3],
            "two": delay_get[4],
            "three": delay_get[5]
        },
        "bottom_side": {
            "uptown_nassau": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[24].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
                    "time": f"{masterlistSUBWAY[24].time}m",
                    "branch": branch(masterlistSUBWAY[24].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[25].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
                    "time": f"{masterlistSUBWAY[25].time}m",
                    "branch": branch(masterlistSUBWAY[25].terminus)
                }
            },
            "uptown_lex": {
                "one": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[26].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
                    "time": f"{masterlistSUBWAY[26].time}m",
                    "branch": branch(masterlistSUBWAY[26].terminus)
                },
                "two": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[27].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
                    "time": f"{masterlistSUBWAY[27].time}m",
                    "branch": branch(masterlistSUBWAY[27].terminus)
                },
                "three": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[28].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
                    "time": f"{masterlistSUBWAY[28].time}m",
                    "branch": branch(masterlistSUBWAY[28].terminus)
                },
                "four": {
                    "emblem": f"<img src='/static/svg/{(masterlistSUBWAY[29].route_id).lower()}.svg' style='height: 90%; margin-left: 7px; margin-top: 5%;'>",
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

    return json.dumps(json_string)   

#print(export())
delay()